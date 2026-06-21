import Header from "./Header";
import Home from "./Home";
import Strategy from "./Strategy"; 
import Pipeline from "./Pipeline";
// import Footer from "./Footer";

export default function LandingPage() {
  return (
    <>
      <Header />

      <main className="pt-24">
        <section id="home">
          <Home />
        </section>

        <section id="strategy">
          <Strategy />
        </section>

        <section id="pipeline">
          <Pipeline />
        </section>

        {/* <Footer /> */}
      </main>
    </>
  );
}
