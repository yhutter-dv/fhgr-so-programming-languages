import { Head } from "$fresh/runtime.ts";
import IconBrandGithub from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/brand-github.tsx";
import IconFaceIdError from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/face-id-error.tsx";
import { type PageProps } from "$fresh/server.ts";
import { load } from "https://deno.land/std@0.210.0/dotenv/mod.ts";
import GitRepoList from "../islands/GitRepoList.tsx";
import { FreshContext } from "$fresh/server.ts";
import { EnvConfig } from "../models/envConfig.ts";

export default async function GitRepos(_req: Request, ctx: FreshContext) {
  const env = await load();
  const config: EnvConfig = {
    apiUrl: env["API_URL"],
  };
  const selectedLanguage = ctx.url.searchParams.get("programmingLanguage");
  const hasValidLanguage = selectedLanguage !== null && selectedLanguage !== "";

  // Header which should be displayed no no programming language was provided as a search parameter.
  const noLanguageHeader = (
    <>
      <Head>
        <title>GitRepos - No Programming Language</title>
      </Head>
      <div class="px-4 py-8 mx-auto bg-slate-50">
        <div class="max-w-screen-md mx-auto flex flex-col items-center justify-center text-center">
          <IconFaceIdError class="w-12 h-12" />
          <h2 class="text-2xl font-bold my-4">Uh oh!</h2>
          <h3 class="text-xl">
            Looks like you did not provide a Programming Language. Please
            revisit this site by clicking on the Link of a Card on the{" "}
            <a href="/" class="underline">Home Page</a>{" "}
            or providing a the query parameter{" "}
            <code>programmingLanguage=YourLanguage</code>
          </h3>
        </div>
      </div>
    </>
  );

  const header = (
    <div class="px-4 py-8 mx-auto bg-slate-50">
      <div class="max-w-screen-md mx-auto flex flex-col items-center justify-center text-center">
        <IconBrandGithub class="w-12 h-12" />
        <h2 class="text-2xl font-bold my-4">
          Popular GitRepos for {selectedLanguage}
        </h2>
        <h3 class="text-xl">
          The Repos were retrieved with the{" "}
          <a
            class="underline underline-offset-2 decoration-2 hover:text-sky-500 ease-in duration-150"
            href="https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-repositories"
            target="_blank"
          >
            GitHub Search API
          </a>. Please do not that the Repos listed here are a Snapshot from the
          Time the Ontology was create with the file{" "}
          <code>knowledge_engineering_extraction.py</code>{" "}
          and may therefore not be up to date.
        </h3>
      </div>
    </div>
  );

  return (
    <>
      {hasValidLanguage
        ? (
          <>
            {header}
            <GitRepoList language={selectedLanguage} config={config} />
          </>
        )
        : noLanguageHeader}
    </>
  );
}
