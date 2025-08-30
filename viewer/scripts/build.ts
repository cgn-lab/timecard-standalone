import { build } from "bun";

await build({
  entrypoints: ["./src/index.ts"],
  outdir: "dist",
  naming: "[dir]/bundle.[ext]",
  minify: false,
  sourcemap: true,
  target: "browser",
  format: "esm",
});
