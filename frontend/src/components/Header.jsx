import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();
  const isOnDemoPage = location.pathname === "/demo";

  const handleLogoClick = (e) => {
    e.preventDefault();

    if (location.pathname === "/") {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    } else {
      navigate("/");
    }
  };

  return (
    <header className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
      <div className="flex items-center justify-between px-gutter py-md max-w-7xl mx-auto">
        {/* Logo */}
        <Link
          to="/"
          onClick={handleLogoClick}
          className="flex items-center gap-sm cursor-pointer no-underline"
        >
          <span
            className="material-symbols-outlined text-primary"
            style={{ fontVariationSettings: '"FILL" 1' }}
          >
            shield
          </span>

          <span className="font-headline font-bold text-3xl tracking-tight text-on-surface">
            reZolve
          </span>
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-lg">
          <nav className="hidden md:flex items-center gap-8 mr-4">
            <a
              href="#strategy"
              className="font-body text-[14px] font-medium text-[#5c3f40] hover:text-primary transition-colors duration-300"
            >
              Strategy
            </a>

            <a
              href="#pipeline"
              className="font-body text-[14px] font-medium text-[#5c3f40] hover:text-primary transition-colors duration-300"
            >
              Pipeline
            </a>
          </nav>

          {!isOnDemoPage && (
            <button
              onClick={() => navigate("/demo")}
              className="bg-primary text-white px-lg py-2.5 rounded-lg font-headline font-semibold text-[14px] hover:bg-primary/90 transition-all shadow-sm cursor-pointer"
            >
              Launch Demo
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
