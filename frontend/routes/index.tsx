import { ProgrammingLanguage } from "../models/programmingLanguage.ts";
import { ProgrammingLanguageCard } from "../components/ProgrammingLanguageCard.tsx";
import { Badge } from "../components/Badge.tsx";
import { Head } from "$fresh/runtime.ts";
import { load } from "https://deno.land/std@0.210.0/dotenv/mod.ts";

export default async function Index() {
  const env = await load();
  const API_URL = env["API_URL"];

  const getProgrammingLanguagesPeopleWantToWorkWith = async (): Promise<
    ProgrammingLanguage[]
  > => {
    const response = await fetch(
      `${API_URL}/languages_people_want_to_work_with`,
    );
    return await response.json() as Promise<
      ProgrammingLanguage[]
    >;
  };

  const getProgrammingLanguagesPeopleHaveWorkedWith = async (): Promise<
    ProgrammingLanguage[]
  > => {
    const response = await fetch(
      `${API_URL}/languages_people_have_worked_with`,
    );
    return await response.json() as Promise<
      ProgrammingLanguage[]
    >;
  };

  const languagesPeopleWantToWorkWith =
    await getProgrammingLanguagesPeopleWantToWorkWith();

  const languagesPeopleHaveWorkedWith =
    await getProgrammingLanguagesPeopleHaveWorkedWith();

  return (
    <>
      <Head>
        <title>Home</title>
      </Head>
      <div class="px-4 py-8 mx-auto bg-slate-50">
        <div class="max-w-screen-md mx-auto flex flex-col items-center justify-center text-center">
          <h2 class="text-2xl font-bold my-4">What is it?</h2>
          <h3 class="text-xl">
            The purpose of this project is to gain Insights into the{" "}
            <a
              class="underline underline-offset-2 decoration-2 hover:text-sky-500 ease-in duration-150"
              href="https://insights.stackoverflow.com/survey/"
              target="_blank"
            >
              Stack Overflow Developer Survey
            </a>{" "}
            from the year 2023. This is achieved by utilizing{" "}
            Knowledge Extraction as well as Knowledge Engineering with the Help
            of{" "}
            <a
              class="underline underline-offset-2 decoration-2 hover:text-sky-500 ease-in duration-150"
              href="https://www.wikidata.org/wiki/Wikidata:Main_Page"
              target="_blank"
            >
              WikiData
            </a>{" "}
            and{"  "}
            <a
              class="underline underline-offset-2 decoration-2 hover:text-sky-500 ease-in duration-150"
              href="https://github.com/"
              target="_blank"
            >
              GitHub
            </a>.
          </h3>
        </div>
      </div>

      <div class="mx-2">
        <h4 class="text-2xl text-center font-bold my-8">
          Programming Languages <Badge text="People want to work in" />
        </h4>

        <div class="grid grid-cols-3 grid-flow-row gap-4 my-4">
          {languagesPeopleWantToWorkWith.map((l) => (
            <ProgrammingLanguageCard programmingLanguage={l} />
          ))}
        </div>

        <h4 class="text-2xl text-center font-bold my-8">
          Programming Languages <Badge text="People have worked with" />
        </h4>

        <div class="grid grid-cols-3 grid-flow-row gap-4 my-4">
          {languagesPeopleHaveWorkedWith.map((l) => (
            <ProgrammingLanguageCard programmingLanguage={l} />
          ))}
        </div>
      </div>
    </>
  );
}
