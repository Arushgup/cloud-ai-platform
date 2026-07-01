export default function Navbar() {
  const email = localStorage.getItem("email");

  return (
    <header className="flex items-center justify-between border-b bg-white px-8 py-5">

      <div>

        <h1 className="text-3xl font-bold">
          Dashboard
        </h1>

        <p className="text-gray-500">
          Welcome back {email ?? "User"} 👋
        </p>

      </div>

    </header>
  );
}