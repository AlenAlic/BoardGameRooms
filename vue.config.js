// Version used for forcing file cache invalidation in exceptional cases
const VERSION = "1";

module.exports = {
  transpileDependencies: ["vuetify"],
  productionSourceMap: false,
  chainWebpack: config => {
    if (process.env.NODE_ENV === "production") {
      // Add version suffix to file names to force cache invalidation (CDN, Browser, and SW) in exceptional cases
      config.output.filename(`js/[name].[contenthash:8].v${VERSION}.js`);
      config.output.chunkFilename(`js/[name].[contenthash:8].v${VERSION}.js`);
    }
    // Don't copy over .example filesp
    config.plugin("copy").tap(([options]) => {
      options[0].ignore.push("*.example");
      return [options];
    });
  },
  css: {
    extract:
      process.env.NODE_ENV === "production"
        ? {
            filename: `css/[name].[contenthash:8].v${VERSION}.css`,
            chunkFilename: `css/[name].[contenthash:8].v${VERSION}.css`
          }
        : undefined
  }
};
