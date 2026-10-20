import { HtmlBasePlugin } from "@11ty/eleventy";

export default function (eleventyConfig) {
  // Prefixes root-relative links, images, css and scripts with pathPrefix.
  eleventyConfig.addPlugin(HtmlBasePlugin);
  eleventyConfig.addPassthroughCopy("src/img");
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/favicon.svg");

  eleventyConfig.addFilter("isoDate", (d) => d.toISOString().slice(0, 10));
  eleventyConfig.addFilter("longDate", (d) =>
    d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" })
  );
  // Newest first, grouped as [[year, [posts...]], ...]
  eleventyConfig.addFilter("groupByYear", (posts) => {
    const sorted = [...posts].sort((a, b) => b.date - a.date);
    const groups = new Map();
    for (const p of sorted) {
      const y = p.date.getUTCFullYear();
      if (!groups.has(y)) groups.set(y, []);
      groups.get(y).push(p);
    }
    return [...groups];
  });

  return {
    dir: { input: "src", output: "_site" },
    pathPrefix: "/blog/",
    // Posts contain Helm/Go template syntax ({{ }}); never run Markdown through a template engine.
    markdownTemplateEngine: false,
  };
}
