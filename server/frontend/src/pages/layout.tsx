import React, { ReactNode } from "react";
import Wrapper from "../components/wrapper";
interface Props {
  children?: ReactNode;
}
export default function Layout({ children }: Props) {
  return (
    <>
      <div>
        <Wrapper />
        <main>{children}</main>
      </div>
    </>
  );
}
