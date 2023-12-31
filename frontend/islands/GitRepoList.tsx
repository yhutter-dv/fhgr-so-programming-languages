import { useEffect, useState } from "preact/hooks";
import { GitRepoCard } from "../components/GitRepoCard.tsx";
import { GitRepo } from "../models/gitRepo.ts";
import { GitRepoRequest } from "../models/gitRepoRequest.ts";
import IconMoodSad from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/mood-sad.tsx";
import { EnvConfig } from "../models/envConfig.ts";
type Props = {
  language: string;
  config: EnvConfig;
};

export default function GitRepoList({ language, config }: Props) {
  const [repos, setRepos] = useState<GitRepo[]>([]);

  useEffect(() => {
    if (language) {
      getGitReposForLanguage(language);
    }
  }, []);

  async function getGitReposForLanguage(language: string) {
    const requestParams: GitRepoRequest = {
      language,
    };
    const response = await fetch(
      `${config.apiUrl}/git_repos/`,
      {
        method: "POST",
        body: JSON.stringify(requestParams),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
      },
    );
    const result = await response.json() as GitRepo[];
    console.log(result);
    setRepos([...result]);
  }

  return (
    <>
      {repos.length === 0
        ? (
          <div class="flex flex-col justify-center text-center items-center">
            <IconMoodSad class="w-12 h-12 my-2" />
            <p>
              No Repos could be found for language {language}
            </p>
          </div>
        )
        : (
          <div class="grid grid-cols-3 grid-flow-row gap-4 my-4">
            {repos.map((r) => <GitRepoCard repo={r} />)}
          </div>
        )}
    </>
  );
}
