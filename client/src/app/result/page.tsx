import React, { useEffect } from "react";
import { getAuthSession } from "@/lib/nextauth";
import { redirect } from "next/navigation";
import ResultCard from "@/components/ResultCard";
import { useDataOutput } from "@/hooks/useDataOutput";

export const metadata = {
  title: "Result | MirrorScripts",
  description: "Automatically generate the report with reference!",
};

interface Props {
  searchParams: {
    resultId?: string;
  };
}

const Result = async ({ searchParams }: Props) => {
  const session = await getAuthSession();
  if (!session?.user) {
    redirect("/");
  }

  return <ResultCard />;
};

export default Result;