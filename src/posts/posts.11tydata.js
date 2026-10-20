// A function (not a template string): markdownTemplateEngine is off, so "{{ }}" permalinks would not be evaluated.
export default {
  eleventyComputed: {
    permalink: (data) => `/posts/${data.page.fileSlug}/index.html`,
  },
};
