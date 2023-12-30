import { GitRepo } from "../models/gitRepo.ts";
import { Badge } from "./Badge.tsx";

type Props = {
  repo: GitRepo;
};

export function GitRepoCard({ repo }: Props) {
  return (
    <div class="shadow flex flex-col p-4">
      <div class="flex flex-row items-center justify-end">
        <Badge text={`${repo.numberOfStars}`} /> Stars
      </div>

      <a
        class="text-xl font-bold underline"
        href={repo.url}
        target="_blank"
      >
        {repo.name}
      </a>

      <div class="my-4">
        <h2 class="text-lg font-bold mb-2">
          Description
        </h2>

        <div>
          {repo.description}
        </div>
      </div>
    </div>
  );
}
