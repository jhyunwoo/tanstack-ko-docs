import { compileMDX } from "next-mdx-remote/rsc";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypePrettyCode from "rehype-pretty-code";
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";
import { visit } from "unist-util-visit";

import type { DocPageData } from "@/lib/docs";
import { rewriteMarkdownHref } from "@/lib/docs";
import { mdxComponents } from "@/components/mdx-components";

function createLinkRewritePlugin(currentOutputPath: string) {
  return function remarkRewriteLinks() {
    return function transformer(tree: Parameters<typeof visit>[0]) {
      visit(tree, "link", (node: { url?: string }) => {
        if (typeof node.url === "string") {
          node.url = rewriteMarkdownHref(node.url, currentOutputPath);
        }
      });
    };
  };
}

const prettyCodeOptions = {
  keepBackground: false,
  theme: {
    dark: "github-dark",
    light: "github-light",
  },
};

export async function renderDocContent(doc: DocPageData) {
  const rendered = await compileMDX({
    source: doc.rawContent,
    components: mdxComponents,
    options: {
      parseFrontmatter: false,
      mdxOptions: {
        format: "md",
        remarkPlugins: [remarkGfm, createLinkRewritePlugin(doc.outputPath)],
        rehypePlugins: [
          rehypeSlug,
          [
            rehypeAutolinkHeadings,
            {
              behavior: "append",
              properties: {
                className: ["anchor-link"],
              },
              content: {
                type: "text",
                value: "#",
              },
            },
          ],
          [rehypePrettyCode, prettyCodeOptions],
        ],
      },
    },
  });

  return rendered.content;
}
