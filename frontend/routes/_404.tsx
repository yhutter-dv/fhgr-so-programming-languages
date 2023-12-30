import { Head } from "$fresh/runtime.ts";
import IconError404 from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/error-404.tsx";

export default function Error404() {
  return (
    <>
      <Head>
        <title>404 - Page not found</title>
      </Head>
      <div class="px-4 py-8 mx-auto bg-slate-50">
        <div class="max-w-screen-md mx-auto flex flex-col items-center justify-center">
          <IconError404 class="w-12 h-12" />
          <h1 class="text-4xl font-bold">Page not found</h1>
          <p class="my-4">
            The page you were looking for doesn't exist.
          </p>
          <a href="/" class="underline">Go back home</a>
        </div>
      </div>
    </>
  );
}
