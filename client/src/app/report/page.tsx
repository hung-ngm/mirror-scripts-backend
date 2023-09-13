import React from "react";

import { getAuthSession } from "@/lib/nextauth";
import { redirect } from "next/navigation";
import ReportCreation from "@/components/forms/ReportCreation";

export const metadata = {
  title: "Report | MirrorScripts",
  description: "Automatically generate the report with reference!",
};

interface Props {
  searchParams: {
    topic?: string;
  };
}

const Report = async ({ searchParams }: Props) => {
  const session = await getAuthSession();
  if (!session?.user) {
    redirect("/");
  }
  return <ReportCreation topic={searchParams.topic ?? ""} />;
};

export default Report;