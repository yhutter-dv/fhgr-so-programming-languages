import { Head } from "$fresh/runtime.ts";
import IconBrandGithub from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/brand-github.tsx";
import { GitRepo } from "../../models/gitRepo.ts";
import { load } from "https://deno.land/std@0.210.0/dotenv/mod.ts";
import { GitRepoRequest } from "../../models/gitRepoRequest.ts";
import { GitRepoCard } from "../../components/GitRepoCard.tsx";
import { type PageProps } from "$fresh/server.ts";
import IconMoodSad from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/mood-sad.tsx";

export default async function GitRepos({ url }: PageProps) {
  const env = await load();
  const API_URL = env["API_URL"];
  const urlParts = url.toString().split("/");
  const selectedLanguage = urlParts[urlParts.length - 1];

  const getGitReposForLanguage = async (language: string): Promise<
    GitRepo[]
  > => {
    const requestParams: GitRepoRequest = {
      language,
    };
    const response = await fetch(
      `${API_URL}/git_repos/`,
      {
        method: "POST",
        body: JSON.stringify(requestParams),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
      },
    );
    return await response.json() as Promise<
      GitRepo[]
    >;
  };

  const repos = await getGitReposForLanguage(selectedLanguage);
  const hasRepos = repos?.length > 0;

  return (
    <>
      <Head>
        <title>GitRepos for Language {selectedLanguage}</title>
      </Head>
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
            </a>. Please do not that the Repos listed here are a Snapshot from
            the Time the Ontology was create with the file{" "}
            <code>knowledge_engineering_extraction.py</code>{" "}
            and may therefore not be up to date.
          </h3>
        </div>
      </div>

      <div class="grid grid-cols-3 grid-flow-row gap-4 my-4">
        {repos.map((r) => <GitRepoCard repo={r} />)}
      </div>

      {hasRepos === false
        ? (
          <div class="flex flex-col justify-center text-center items-center">
            <IconMoodSad class="w-12 h-12 my-2" />
            <p>
              No Repos could be found for language {selectedLanguage}
            </p>
          </div>
        )
        : ""}
    </>
  );
}
