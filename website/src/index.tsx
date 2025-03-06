/* @refresh reload */
import { render } from 'solid-js/web';
import { Route, Router } from "@solidjs/router";
import './index.css';
import App from './App';
import Home from './pages/home';
import Page404 from './pages/notFound';
import LlmResults from './pages/llmResults';

const root = document.getElementById('root');

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
  throw new Error(
    'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?',
  );
}

render(() => <Router root={App}>
  <Route path={"/"} component={Home} />
  <Route path={"/llm-results"} component={LlmResults} />
  <Route path={"/about"} component={Page404} />
  <Route path="*404" component={Page404} />

</Router>, root!);
