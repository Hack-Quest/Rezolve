// import React from "react";

// export default function Header() {
//   return (
//     <header className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
//       <div className="flex items-center justify-between px-gutter py-md max-w-7xl mx-auto">
//         {/* Brand Logo / Operator Details */}
//         <div className="flex items-center gap-sm">
//           <span
//             className="material-symbols-outlined text-primary"
//             style={{ fontVariationSettings: '"FILL" 1' }}
//           >
//             shield
//           </span>
//           <span className="font-headline font-bold text-xl tracking-tight text-on-surface">
//             reZolve
//           </span>
//         </div>

//         {/* Navigation Links & Action Button */}
//         <div className="flex items-center gap-lg">
//           <nav className="hidden md:flex items-center gap-6 mr-4">
//             <a
//               href="#pipeline"
//               className="font-body text-[14px] font-medium text-[#5c3f40] hover:text-primary transition-colors duration-300"
//             >
//               Pipeline
//             </a>
//             <a
//               href="#strategy"
//               className="font-body text-[14px] font-medium text-[#5c3f40] hover:text-primary transition-colors duration-300"
//             >
//               Strategy
//             </a>
//             <a
//               href="#documentation"
//               className="font-body text-[14px] font-medium text-[#5c3f40] hover:text-primary transition-colors duration-300"
//             >
//               Documentation
//             </a>
//           </nav>

//           <button className="bg-primary text-white px-lg py-2.5 rounded-lg font-headline font-semibold text-[14px] hover:bg-primary/90 transition-all shadow-sm cursor-pointer">
//             Launch Demo
//           </button>
//         </div>
//       </div>
//     </header>
//   );
// }

import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  return (
    <header className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
      <div className="flex items-center justify-between px-gutter py-md max-w-7xl mx-auto">
        {/* Logo/Brand Home Route */}
        <Link
          to="/"
          className="flex items-center gap-sm cursor-pointer decoration-none"
        >
          <span
            className="material-symbols-outlined text-primary"
            style={{ fontVariationSettings: '"FILL" 1' }}
          >
            shield
          </span>
          <span className="font-headline font-bold text-xl tracking-tight text-on-surface">
            reZolve          </span>
        </Link>

        <div className="flex items-center gap-lg">
          <nav className="hidden md:flex items-center gap-6 mr-4">
            {/* Swapped <a> tag with <Link> targeting your dedicated route */}
            <Link
              to="/pipeline"
              className="font-body text-[14px] font-medium text-[#5c3f40] hover:text-primary transition-colors duration-300"
            >
              Pipeline
            </Link>
            <Link
              to="/strategy"
              className="font-body text-[14px] font-medium text-[#5c3f40] hover:text-primary transition-colors duration-300"
            >
              Strategy
            </Link>
            <Link
              to="/documentation"
              className="font-body text-[14px] font-medium text-[#5c3f40] hover:text-primary transition-colors duration-300"
            >
              Documentation
            </Link>
          </nav>

          <button
            className="bg-primary text-white px-lg py-2.5 rounded-lg font-headline font-semibold text-[14px] hover:bg-primary/90 transition-all shadow-sm cursor-pointer"
            onClick={() => navigate("/demo")}
          >
            Launch Demo
          </button>
        </div>
      </div>
    </header>
  );
}
