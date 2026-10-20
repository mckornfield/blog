---
title: "AWS Role Assumption from a GCP VM"
date: 2024-05-02
medium_url: "https://medium.com/@mckornfield/aws-role-assumption-from-a-gcp-vm-5abec58bd450"
---

Now with terraform!

![GCP -> AWS Role assumption](/img/aws-role-assumption-from-a-gcp-vm/1_vkKJ9ZaOIHaOwr_v1BcRwQ.png.png)

*GCP -> AWS Role assumption*

### Didn’t AWS write a Blog on This?

Yes, [right here](https://aws.amazon.com/blogs/security/access-aws-using-a-google-cloud-platform-native-workload-identity). And someone wrote a Medium article on how to do it [here](https://medium.com/google-cloud/how-to-assume-multiple-aws-roles-from-a-gcp-service-account-keyless-595a978eee7b), but there are a few things I think worth calling out/explaining:

- How JWTs work and are encoded in this context
- How the trust relationship is created via attributes of the JWT
- How to create this trust relationship with a Terraform file

### How JWTs Work

A JSON Web Token (JWT) is a way to send information in a way that can be verified by the caller, i.e. you can tell if the token has been tampered with.

If you look at a JWT they are essentially three parts:

1. A header
2. A payload
3. A verifications signature (a hash of the other two sections with a private key)

There’s a great interactive playground on jwt.io you can use to go back and forth between the two formats (the base64urlencoded and the unencoded pieces).

[JWT.IO](https://jwt.io/)

What makes them “work” is a private/public key pair that you can use to ensure the signature is legitimate. This aspect functions in a similar way to SSH or other private/public key trust schemes.

But the other aspect of what can establish “trust” in a JWT is various attributes in the payload, sometimes called “claims.”

For our handy dandy GCP -> AWS setup, there’s three claims from [the JWT token the GCP metadata service creates](https://cloud.google.com/compute/docs/instances/verifying-instance-identity#request_signature) that we’ll utilize.

1. The audience, a field that we’ll explicitly set when making the call (“aud”)
2. The authorized party field (“azp”)
3. The subject field (“sub”)

An example of what this might look like in a decoded token payload:

```json
{
    ...
   "aud": "my-audience-value",
   "sub": "111111",
   "azp": "222222",
    ...
}
```

When you’re on a GCP instance, you can get this token by curling an endpoint.

### The Trust Relationship

You’ll establish trust to the AWS role we create by making a “Federated” principal that maps to “accounts.google.com”. This will allow the

We’ll then check that these three fields match up like so:

- `accounts.google.com:oaud` -> “aud”
- `accounts.google.com:aud` -> “azp”
- `accounts.google.com:sub` -> “sub”

This mapping doesn’t really make much sense to me, but from [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html):

> `aud` for OAuth 2.0 Google client IDs of your application, when the `azp` field is not set. When the `azp` field is set, the `aud` field matches the `accounts.google.com:oaud` condition key.

🤷‍♂

The subject one makes sense though!

### The Terraform to Do It

So hopefully we have a decent idea of what we need to do, here’s terraform that will create an AWS role, with the proper trust, and bind a GCP service account to it via extracting the “sub” and “azp” fields from a token.

An important note: your service account (which you can create manually/via terraform OR use the default service account for the instances) needs to be able to create tokens by [having the following role](https://cloud.google.com/iam/docs/service-account-permissions#token-creator-role) `roles/iam.serviceAccountTokenCreator`

I purposefully did this outside of the terraform since it isn’t atomic (you have to grant the role separately). For the default service account, I had to grant it, but for one I created using terraform there was no issue.

```perl
provider "aws" {
  region = "us-east-1"
  assume_role {
    role_arn = "arn:aws:iam::123456789010:role/Executor"
  }
}

locals {
  project_id      = "my-gcp-project"
  target_audience = "my-audience"
  # This is the format for a default service account, it can be an email
  # or a name reference
  target_service_account = "123123123123-compute@developer.gserviceaccount.com"
}

provider "google" {
  project = "my-gcp-project"
}

data "google_project" "project" {
  project_id = local.project_id
}

# Had to manually "grant target_service_account the roles/iam.serviceAccountTokenCreator role on itself."
# In order to enable this token creation piece
data "google_service_account_id_token" "oidc" {
  target_audience        = local.target_audience
  target_service_account = local.target_service_account
}

locals {
  # For why we have do this extra mangling, it might be instructive to see
  # an example of base64urldecode vs. base64decode
  # e.g., https://github.com/auth0/jwt-decode/blob/main/lib/index.ts#L37
  token_section = format("%s=", split(".", data.google_service_account_id_token.oidc.id_token)[1])
  token_dict    = jsondecode(format("%s}", base64decode(nonsensitive(local.token_section))))
  token_azp     = local.token_dict["azp"]
  token_aud     = local.token_dict["aud"]
  token_sub     = local.token_dict["sub"]
}

resource "aws_iam_role" "cross_cloud_access_s3_role" {
  name = "gcp-to-aws-access"

  assume_role_policy = data.aws_iam_policy_document.gcp_assume_role_policy_doc.json

  managed_policy_arns = [
    aws_iam_policy.allow_bucket_access_policy.arn
  ]
}

resource "aws_iam_policy" "allow_bucket_access_policy" {
  name   = "allow-bucket-access"
  policy = data.aws_iam_policy_document.bucket_read_and_write.json
}



data "aws_iam_policy_document" "bucket_read_and_write" {
  statement {
    sid    = "readBucket"
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:GetObject",
    ]
    resources = [
      "arn:aws:s3:::my-s3-bucket/*",
    ]
  }

  statement {
    sid    = "listBucket"
    effect = "Allow"
    actions = [
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::my-s3-bucket",
    ]
  }
}


data "aws_iam_policy_document" "gcp_assume_role_policy_doc" {
  statement {
    sid    = "AllowGCPAssumeRole"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]
  
  # This allows us to do it specifically from our GCP service account
    principals {
      type        = "Federated"
      identifiers = ["accounts.google.com"]
    }
  
  # This is how we map trust to the token values
    condition {
      test     = "StringEquals"
      variable = "accounts.google.com:aud"
      values   = [local.token_azp]
    }
    condition {
      test     = "StringEquals"
      variable = "accounts.google.com:oaud"
      values   = [local.token_aud]
    }
    condition {
      test     = "StringEquals"
      variable = "accounts.google.com:sub"
      values   = [local.token_sub]
    }
  }
}
```

There’s inline comments, but feel free to comment if something isn’t clear from the previous explanations/ things stated inline.

For the token decoding specifically, this worked for me but [it might need to be tweaked if the payload length doesn’t exactly match up](https://github.com/auth0/jwt-decode/blob/main/lib/index.ts).

Running this terraform requires you to have an AWS role you can assume AND the ability to create a token as that service account user in the GCP project.

### A Slightly Better Bash Script to Assume the Role

There’s a script that will power the GCP -> AWS Role assumption called out in the AWS blog, but it has a few flaws:

1. Its jq manipulation can be simplified/ deserves a bit of explanation
2. It doesn’t unset any `AWS_PROFILE` or `AWS_DEFAULT_PROFILE` env vars, which will cause the script to hang if they’re set during the `assume-role-with-web-identity` call

Here’s my slightly improved version:

```bash
#!/bin/bash
AUDIENCE="my-audience"
# This will call back to the role you created earlier
ROLE_ARN="arn:aws:iam::528917342086:role/123456789010"

instance_url="http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience=${AUDIENCE}&format=full&licenses=FALSE"
jwt_token=$(curl -sH "Metadata-Flavor: Google" "$instance_url")

jwt_sub=$(jq -rR 'split(".") | .[1] | @base64d | fromjson | .sub' <<<"$jwt_token")

# NOTE: These env vars when set interfere with the assume role call
unset AWS_DEFAULT_PROFILE
unset AWS_PROFILE

# We have to set the Version=1 since it's not returned but it is required
aws sts assume-role-with-web-identity --role-arn "$ROLE_ARN" \
    --role-session-name "$jwt_sub" --web-identity-token "$jwt_token" |
    jq '.Credentials' | jq '.Version=1'
```

Note the unsetting of the vars, and the call outs for why the line ends with `jq '.Version=1'`

Assuming you save this script in `/opt/bin/credentials.sh` , this will help you bootstrap the script:

```bash
chmod +x /opt/bin/credentials.sh

profile_name=GcpToAwsRole
aws configure set credential_process "/opt/bin/credentials.sh" --profile "$profile_name"
aws configure set region us-east-1 --profile "$profile_name" # change as appropriate
```

And then `export AWS_DEFAULT_PROFILE=GcpToAwsRole` in your shell, and your SDK/CLI commands should work just fine (noting that the CLI commands will get a new token every time, [but the SDK commands supposedly cache the token](https://aws.amazon.com/blogs/security/access-aws-using-a-google-cloud-platform-native-workload-identity/#:~:text=Note%20that%20AWS,you%20run%20commands)).

Hopefully that helps you in your adventures working within multiple clouds!
