import { Component, lazy, Suspense, useReducer, useRef, useState } from "react";
import GridLoader from "react-spinners/GridLoader";
const Main = lazy(() => import("./Main"));

export { App };

class ErrorBoundary extends Component {
  state = { error: null };

  static getDerivedStateFromError(error) {
    return { error };
  }
  render() {
    const { error } = this.state;
    const { children, fallback } = this.props;
    if (error && !fallback) return <ErrorScreen error={error} />;
    if (error) return <fallback error={error} />;
    return children;
  }
}

function ErrorScreen({ error }) {
  return (
    <div className="error">
      <h3>We are sorry Something went Wrong!!</h3>
      <p>We cannot process your request at this moment</p>
      <p>ERROR: {error}</p>
    </div>
  );
}

function SiteLayout({ children, menu = (_) => null }) {
  return (
    <div className="app">
      <div className="menu">{menu}</div>
      <div className="app-body">{children}</div>
    </div>
  );
}

function BreakCallout({ raise = false }) {
  if (raise) throw "Callout Broken";
}

function BreakContent({ raise = false }) {
  if (raise) throw "Contents Broken";
}

function BreakMenu({ raise = false }) {
  if (raise) throw "Menu Broken";
}

function Callout({ children }) {
  return (
    <ErrorBoundary>
      <BreakCallout raise={false} />
      <div className="callout">{children}</div>
    </ErrorBoundary>
  );
}

function Agreement({ onAgree = (_) => _ }) {
  return (
    <div className="agreement">
      <h1>
        <center>
          <u>Terms and Conditions</u>
        </center>
      </h1>
      <p>
        Lorem ipsum dolor sit amet consectetur, adipisicing elit. Voluptatibus
        ex eos nam repellendus. Quos dolore nihil eos doloremque accusantium,
        laudantium beatae quae nam corporis voluptas nulla esse, praesentium
        cupiditate est rem officia quibusdam repellendus repudiandae eum
        deserunt tenetur iste? Dolore obcaecati est sit minus deleniti quas ea
        officiis suscipit, ipsam quidem eveniet doloribus? Aliquam quia eaque
        blanditiis accusamus. Asperiores sunt, dignissimos quas veniam sed
        repudiandae illum quidem quis. Ipsam voluptates, fuga exercitationem
        sunt magni quisquam nesciunt! Dignissimos quas ea voluptate, rem
        molestiae, asperiores ex suscipit, maxime deleniti quod ut animi
        impedit. Laboriosam nam suscipit, dolorem porro quidem voluptatem quam
        Lorem ipsum dolor, sit amet consectetur adipisicing elit. Ipsum
        veritatis modi repudiandae unde vero aut consequatur, libero quod illo
        perspiciatis incidunt suscipit quam nulla impedit obcaecati non
        doloribus, officiis voluptatibus est doloremque at mollitia asperiores
        velit quisquam! Quidem totam iste nihil esse dolorem doloremque suscipit
        aperiam, voluptatum cum dolore. Cumque reprehenderit, recusandae quis
        accusamus blanditiis nemo corporis voluptas aut, nostrum officia
        eligendi. Iusto nostrum ea atque dolorum odio nisi ipsum debitis
        quisquam placeat. Facere temporibus excepturi quidem sit at blanditiis
        quis repudiandae, consequatur voluptatem, unde possimus eum delectus
        aperiam? Pariatur temporibus atque porro error optio a at enim impedit
        aut blanditiis, quam repellendus reiciendis nisi. Fuga cupiditate unde
        nobis ducimus reiciendis officia nemo atque ex veritatis libero,
        exercitationem autem dolor culpa id numquam, non optio iure omnis fugit
        a quis iste possimus impedit? Quam doloribus soluta dolores, ad odit
        mollitia eligendi quae quidem earum iusto saepe ex? Ducimus, autem
        necessitatibus atque iusto velit eligendi reiciendis minima temporibus!
        Id aspernatur tempora veniam illum fuga, sed aut architecto velit
        voluptatem recusandae obcaecati voluptates dolorum error iste
        consequuntur, beatae animi at? Consectetur commodi quisquam libero quos,
        fugiat doloribus deleniti. Deleniti eveniet, placeat sed perferendis,
        saepe odio debitis dolore pariatur, cumque in earum? Neque.
      </p>
      <div className="btn btn-primary" onClick={onAgree}>
        Agree
      </div>
    </div>
  );
}

function AppComponent() {
  const [agree, setAgree] = useReducer((val) => !val, false);
  if (!agree) return <Agreement onAgree={setAgree} />;
  return (
    <ErrorBoundary>
      <Suspense fallback={<GridLoader />}>
        <Main />
      </Suspense>
    </ErrorBoundary>
  );
}

function Layout() {
  return (
    <SiteLayout menu={<p>&lt;Menu /&gt;</p>}>
      <>
        <Callout>&lt;Callout /&gt;</Callout>
        <h1>&lt;Contents /&gt;</h1>
        <p>This is the main part.</p>
        <AppComponent />
      </>
    </SiteLayout>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <Layout />
    </ErrorBoundary>
  );
}
