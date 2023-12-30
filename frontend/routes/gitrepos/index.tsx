import { Head } from "$fresh/runtime.ts";
import IconFaceIdError from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/face-id-error.tsx";
export default function GitRepoIndex() {
  return (
    <>
      <Head>
        <title>GitRepos - No Programming Language</title>
      </Head>
      <div class="px-4 py-8 mx-auto bg-slate-50">
        <div class="max-w-screen-md mx-auto flex flex-col items-center justify-center text-center">
          <IconFaceIdError class="w-12 h-12" />
          <h2 class="text-2xl font-bold my-4">Uh oh!</h2>
          <h3 class="text-xl">
            Looks like you did not provide a Programming Language. Please visit
            this site with a Programming Language as part of the url. For
            example if you want <code>C++</code> the url should look like this
            {" "}
            <code>/gitrepos/C++</code>
          </h3>
        </div>
      </div>
    </>
  );
}
