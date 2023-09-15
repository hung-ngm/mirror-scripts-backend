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

const markdownContent = `# Research on Travel Industry Report

### Introduction

The travel industry is a significant global economic pillar employing millions of people across numerous countries. It is an industry that is intertwined with various sectors, including accommodation, gastronomy, transportation, and attractions, encompassing small local businesses through to multinational corporations. This industry has been severely affected by the COVID-19 pandemic around the globe, consequently impacting national economies. This report aims to provide an analysis of the current status, market trends, and future prospects of the travel industry, focusing on multiple data sources and reports.

### The Impact of Covid-19 on the Travel Industry

The pandemic’s impact on the travel industry was severe (National Geographic, n.d.). According to the World Travel and Tourism Council, the potential job loss may amount to 75 million globally with a possible revenue loss of $2.1 trillion. Airlines are expected to lose at least $250 billion, and hotel occupancy rates have significantly declined, leading to substantial revenue losses. 

According to the World Tourism Organization (UNWTO), international tourist arrivals increased only by 4% in 2021 compared to the pre-pandemic levels in 2019. This translates to more than 1 billion fewer international arrivals. Based on the UNWTO Panel of Experts' forecast, the earliest full recovery of the travel industry is expected to be around 2024 or later (World Economic Forum, 2022).

In the U.S, the U.S Census Bureau's Quarterly Workforce Indicators highlighted that travel, tourism, and outdoor recreation workers experienced significant earnings losses in the second quarter of 2020, up to 40% compared to the same period the previous year (U.S. Census Bureau, 2021).

### The Status of the Travel Industry

According to the Centralized Recovery and Growth Insights Dashboard developed by U.S. Travel in partnership with Tourism Economics, tools are now available to track the industry's performance, travel volumes, and predictive indicators of recovery. This database includes over 20 sources for data, giving a comprehensive picture of the state of the travel industry (U.S. Travel, n.d.). A variety of market research reports are also available, providing a synopsis of economic, consumer, and travel performance, with in-depth examinations of current traveler behavior and shifts in trends. 

On the other hand, Phocuswright, a leading travel industry research authority, provides market research reports spanning consumer research, distribution and marketing, technology innovation, among other critical elements informing the future direction of the industry (Phocuswright, n.d.). 

### Current Trends and Changes in the Travel Industry

The COVID-19 pandemic has brought about changes in the travel industry. There is a strong desire among Americans to travel and make up for lost time (NPR, 2021). However, travelers are shifting their preferences from city-centered hotel stays and international travel to outdoor experiences and rural areas. 

A recovery of the travel industry is underway, as stated by the U.S. Travel Association, and the rollout of vaccinations has significantly contributed to increasing travel. Popular destinations now include coastal areas, small towns, ski destinations (NPR, 2021). Moreover, there is a renewed focus on sustainability in travel, with more than a third of US adults willing to pay more for a sustainable vacation (YouGov, 2021). 

### Future outlook

Despite the devastating impacts of the pandemic, the future outlook for the travel industry is positive (CNBC, 2021). There is an anticipation of a rise in tourism in 2022 thanks to governmental actions worldwide to revive travel industry sectors. Nonetheless, the ongoing pandemic and the emergence of new variants like Omicron are expected to continue affecting the industry's outlook.

Moreover, as countries relax their travel restrictions, like China, there is an expected increase in travel and tourism, both domestically and internationally (Statista, n.d.). Interestingly, we see that the revenge travel trend, a phenomenon where people are eager to make up for lost vacation time due to pandemic restrictions, is emerging as a significant post-pandemic travel trend (Statista, n.d.).

### Conclusion

Fine while the travel industry was dramatically impacted by the COVID-19 pandemic with contractions reported across the globe, there are several positive indicators pointing towards recovery. Initiatives like regular high-frequency intelligence tracking, identification of new market trends, and a renewed focus on sustainability demonstrate the sector's adaptability to unprecedented situations. While there are predictions for the travel industry returning to pre-pandemic levels in 2024, continuous monitoring of trends and swift adaptations will play key roles in reshaping the sector and aid in expedited recovery. Despite the challenges faced, the travel industry continues to persist as an integral part of the global economy.

### References
National Geographic. (n.d.). How COVID-19 impacted the travel industry. Retrieved from https://www.nationalgeographic.com/travel/article/how-coronavirus-is-impacting-the-travel-industry

CNBC. (2021). 4 charts show what the travel industry looks like 2 years into Covid. Retrieved from https://www.cnbc.com/2021/12/15/4-charts-show-what-the-travel-industry-looks-like-2-years-into-covid.html

NPR. (2021). Pandemic Travel. Retrieved from https://www.npr.org/2021/10/09/1036555480/pandemic-travel-industry-tourism-vacations

Phocuswright. (n.d.). Homepage. Retrieved from https://www.phocuswright.com/

Statista. (n.d.). Impact of the coronavirus pandemic on the global economy - Statistics & Facts. Retrieved from https://www.statista.com/topics/6184/coronavirus-covid-19-impact-on-the-global-economy

U.S. Travel. (n.d.). Recovery and Growth Insights Dashboard. Retrieved from https://www.ustravel.org/research/monthly-travel-data-report

U.S. Census Bureau. (2021). Initial Impact of COVID-19 on Travel, Tourism, Outdoor Recreation Varied Widely Across States. Retrieved from https://www.census.gov/library/stories/2021/06/initial-impact-of-covid-19-on-travel-tourism-outdoor-recreation-varied-widely-across-states.html

World Economic Forum. (2022). What the year ahead could look like for the world's travel and tourism sector. Retrieved from https://www.weforum.org/agenda/2022/01/global-travel-tourism-pandemic-covid-19

YouGov. (2021). Travel and Tourism Insights 2021 survey. Retrieved from https://today.yougov.com/topics/travel/articles-reports/2021/12/13/travel-and-tourism-insights-2021-survey`;

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


