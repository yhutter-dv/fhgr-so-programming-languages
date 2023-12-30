import IconBrandStackoverflow from "https://deno.land/x/tabler_icons_tsx@0.0.5/tsx/brand-stackoverflow.tsx";
type Props = {
  active: string;
};

export function Header({ active }: Props) {
  const menus = [
    { name: "Home", href: "/" },
    { name: "GitRepos", href: "/gitrepos" },
  ];

  const isMatch = (href: string, active: string): boolean => {
    if (href === "/") {
      return href === active;
    }
    return active.includes(href);
  };

  return (
    <div class="bg-white w-full py-6 px-8 flex flex-col sm:flex-row items-center gap-4">
      <div class="flex items-center flex-1">
        <IconBrandStackoverflow class="w-12 h-12" />
        <div class="text-2xl ml-1 font-bold">
          Stackoverflow Knowledge Insights
        </div>
      </div>
      <ul class="flex items-center gap-6">
        {menus.map((menu) => (
          <li>
            <a
              href={menu.href}
              class={"text-gray-500 hover:text-gray-700 py-1 border-gray-500" +
                (isMatch(menu.href, active) ? " font-bold border-b-2" : "")}
            >
              {menu.name}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
