import React from "react";
import { AppProps } from "next/app";
import "./styles.css";
import Layout from "./layout";

// eslint-disable-next-line
function MyApp({ Component, pageProps }: AppProps) {
  const AnyComponent = Component as any;
  return (
    <Layout>
      <AnyComponent {...pageProps} />
    </Layout>
  );
}

export default MyApp;
