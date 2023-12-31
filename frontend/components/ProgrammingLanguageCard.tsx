import { ProgrammingLanguage } from "../models/programmingLanguage.ts";

type Props = {
  programmingLanguage: ProgrammingLanguage;
};

export function ProgrammingLanguageCard({ programmingLanguage }: Props) {
  const gitRepoUrl =
    `/gitrepos?programmingLanguage=${programmingLanguage.name}`;
  const hasUseCases = programmingLanguage.useCases?.length > 0;
  const hasParadigms = programmingLanguage.paradigms?.length > 0;
  const hasInfluences = programmingLanguage.influences?.length > 0;
  return (
    <div class="shadow flex flex-col p-4">
      <div class="flex flex-row justify-between">
        <h1 class="text-xl font-bold">
          {programmingLanguage.name}
        </h1>
        <a class="underline underline-offset-1" href={gitRepoUrl}>
          See popular GitRepos
        </a>
      </div>

      <div class="my-4">
        <h2 class="text-lg font-bold mb-2">
          Paradigms
        </h2>

        <div>
          {hasParadigms
            ? programmingLanguage.paradigms.map((p) => (
              <a
                class="inline-block p-2 mr-2 mb-2 font-bold text-sm bg-slate-50 hover:bg-slate-200 ease-in duration-150 rounded"
                href={p.url}
                target="_blank"
              >
                #{p.name}
              </a>
            ))
            : (
              <p>
                No Paradigms found...
              </p>
            )}
        </div>
      </div>

      <div class="my-4">
        <h2 class="text-lg font-bold mb-2">
          Use Cases
        </h2>

        <div>
          {hasUseCases
            ? programmingLanguage.useCases.map((u) => (
              <a
                class="inline-block p-2 mr-2 mb-2 font-bold text-sm bg-slate-50 hover:bg-slate-200 ease-in duration-150 rounded"
                href={u.url}
                target="_blank"
              >
                #{u.name}
              </a>
            ))
            : (
              <p>
                No Use Cases found...
              </p>
            )}
        </div>
      </div>

      <div class="my-4">
        <h2 class="text-lg font-bold mb-2">
          Influences
        </h2>

        <div>
          {hasInfluences
            ? programmingLanguage.influences.map((i) => (
              <a
                class="inline-block p-2 mr-2 mb-2 font-bold text-sm bg-slate-50 hover:bg-slate-200 ease-in duration-150 rounded"
                href={i.url}
                target="_blank"
              >
                #{i.name}
              </a>
            ))
            : (
              <p>
                No Influences found...
              </p>
            )}
        </div>
      </div>
    </div>
  );
}
