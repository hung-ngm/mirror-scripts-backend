"use client";
import { reportCreationSchema } from "@/schemas/forms/report";
import React, { useState, useEffect } from "react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
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
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import showdown from 'showdown';
import axios, { AxiosError } from "axios";
import { useMutation } from "@tanstack/react-query";
import { useToast } from "../ui/use-toast";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useDataOutput } from "@/hooks/useDataOutput";
import LoadingReport from "../LoadingReport";
import useWebsocket from "@/hooks/useWebsocket";

type Props = {
  topic: string;
};

type Input = z.infer<typeof reportCreationSchema>;

const ReportCreation = ({ topic: topicParam }: Props) => {
  const [isLoading, setIsLoading] = useState(false);
  // const [dataOutput, setDataOutput] = useState("");
  const router = useRouter();
  const { dataOutput, setDataOutput } = useDataOutput();
  const { send, close, socketRef } = useWebsocket();

  useEffect(() => {
    const socket = socketRef.current;

    // Send a ping message every 5 seconds
    // const intervalId = setInterval(() => {
    //   send(JSON.stringify({ type: 'ping' }));
    // }, 5000);

    socket.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data);

      // if (data.type === 'ping') {
      //   send(JSON.stringify({ type: 'pong' }));
      // } else
     
      if (data.type === 'logs') {
        // Update your component's state with the new log message
        console.log("logs: ", data);
        setIsLoading(true);
    
        if (data.output.startsWith("\nTotal run time:")) {
          router.push('/result');
          setFinishedLoading(true);
          setIsLoading(false);
        }
      } else if (data.type === 'report') {
        setDataOutput((prevDataOutput: string) => prevDataOutput + data.output);
        console.log("report: ", data.output);
        console.log(dataOutput);
      } else if (data.type === 'path') {
        // Update your component's state with the new download link
        console.log("path: ", data);
      }
    };
    

    return () => {
      // clearInterval(intervalId);
      close();
    }
  }, [])

  const [showLoader, setShowLoader] = useState(false);
  const [finishedLoading, setFinishedLoading] = useState(false);
  const { toast } = useToast();
  // const { mutate: getQuestions, isLoading } = useMutation({
  //   mutationFn: async ({ topic, reportType }: Input) => {
  //     const response = await axios.post("/api/game", { topic, reportType });
  //     return response.data;
  //   },
  // });
  

  const form = useForm<Input>({
    resolver: zodResolver(reportCreationSchema),
    defaultValues: {
      task: topicParam,
      report_type: "research_report",
      agent: "Auto Agent"
    },
  });

  const onSubmit = async (data: Input) => {
    setShowLoader(true);
    // getQuestions(data, {
    //   onError: (error) => {
    //     setShowLoader(false);
    //     if (error instanceof AxiosError) {
    //       if (error.response?.status === 500) {
    //         toast({
    //           title: "Error",
    //           description: "Something went wrong. Please try again later.",
    //           variant: "destructive",
    //         });
    //       }
    //     }
    //   },
    //   onSuccess: ({ gameId }: { gameId: string }) => {
    //     setFinishedLoading(true);
    //     // setTimeout(() => {
    //     //   if (form.getValues("type") === "mcq") {
    //     //     router.push(`/play/mcq/${gameId}`);
    //     //   } else if (form.getValues("type") === "open_ended") {
    //     //     router.push(`/play/open-ended/${gameId}`);
    //     //   }
    //     // }, 2000);
    //   },
    // });

    // });
    // if (finishedLoading) {
    //   router.push({
    //     pathname: '/result',
    //     query: { dataOutput },
    //   });
    // };

    console.log(data);
    send(`start ${JSON.stringify(data)}`);
  };
  form.watch();

  if (showLoader) {
    return <LoadingReport finished={finishedLoading} />;
  }

  return (
    <div className="absolute -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 w-3/5">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Generate a report</CardTitle>
          <CardDescription>Provide the topic</CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              <FormField
                control={form.control}
                name="task"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Topic</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter a topic" {...field} />
                    </FormControl>
                    <FormDescription>
                      Please provide any topic you would like to automatically generate a report on.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="report_type"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Select the type of report</FormLabel>
                    <FormControl>
                      <Select
                        onValueChange={(value) => {
                          form.setValue("report_type", value);
                        }}
                      >
                        <SelectTrigger className="w-[180px]">
                          <SelectValue placeholder="Select a report type" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectGroup>
                            <SelectLabel>Report Types</SelectLabel>
                            <SelectItem value="research_report">Research Report</SelectItem>
                            <SelectItem value="resource_report">Resource Report</SelectItem>
                            <SelectItem value="outline_report">Outline Report</SelectItem>
                          </SelectGroup>
                        </SelectContent>
                      </Select>
                    </FormControl>

                    <FormDescription>
                      You can choose the type of report you want to generate automatically here.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button disabled={isLoading} type="submit">
                Generate
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
};

export default ReportCreation;