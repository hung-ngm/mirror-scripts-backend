"use client";
import React from "react";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
  } from "@/components/ui/form";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import ReactMarkdown from "react-markdown";
import { useDataOutput } from "@/hooks/useDataOutput";
import Showdown from 'showdown';

// type Props = {
//   resultId: string;
// }

const ResultCard = () => {
  const { dataOutput } = useDataOutput();
  const converter = new Showdown.Converter();

  return (
    <div className="absolute -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 w-3/5">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Report generated</CardTitle>
        </CardHeader>

          <ScrollArea className="h-[500px] text-lg text-gray-700 bg-white p-4 rounded flex items-center justify-center">
            <div className="prose max-w-full p-4">
              <ReactMarkdown>{dataOutput}</ReactMarkdown>
            </div>
          </ScrollArea>

      </Card>
    </div>
  )
};

export default ResultCard;


