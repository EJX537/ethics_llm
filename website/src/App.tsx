import { A } from '@solidjs/router';
import type { Component, JSX } from 'solid-js';

const App: Component = (props: { children?: JSX.Element }) => {
  return (
    <div class='flex flex-col h-screen w-screen overflow-auto'>
      <div class='flex w-full h-16 bg-blue-400 bg-gradient-to-b to-blue-700'>
        <div class='flex w-full justify-center items-center text-3xl font-medium h-16'>
          Offensive AI Ethics
        </div>
      </div>
      <div class='flex w-full bg-blue-700 bg-gradient-to-r to-blue-500 justify-center text-slate-300'>
        <ul class='flex justify-between w-1/3'>
          <li class='hover:text-slate-100'>
            <A href="/">Home</A>
          </li>
          <li class='hover:text-slate-100'>
            <A href="/llm-results">LLM Alignment Results</A>
          </li>
          <li class='hover:text-slate-100'>
            <A href="/about">About</A>
          </li>
        </ul>
      </div>
      <main class='flex flex-1 bg-slate-50'>
        {props.children}
      </main>
    </div>
  );
};

export default App;
