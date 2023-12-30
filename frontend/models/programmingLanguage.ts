import { Paradigm } from "./paradigm.ts";
import { UseCase } from "./useCase.ts";

export type ProgrammingLanguage = {
  name: string;
  useCases: UseCase[];
  paradigms: Paradigm[];
  url: string;
  influences: ProgrammingLanguage[];
};
