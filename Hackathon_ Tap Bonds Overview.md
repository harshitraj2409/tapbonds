## **Introduction**

Welcome to the **Tap Bonds Hackathon**, an exciting opportunity for students to build an **AI-powered layer** for bond discovery and research. Your challenge is to enhance the Tap Bonds platform with AI-driven capabilities, making it more interactive, intelligent, and user-friendly.

**What does Tap Bonds do?**

Tap Bonds is a knowledge and research platform that helps users explore, analyze, and track bonds efficiently. It provides detailed ISIN-level bond information, credit ratings, issuer details, and cash flow schedules. The platform simplifies bond discovery and comparison by aggregating data from multiple sources, enabling users to make informed investment decisions. While Tap Bonds does not facilitate bond trading, it serves as a comprehensive resource for bond market research.

**Key features include:**

* **Bond Screener** – A powerful tool that allows users to do Financial Analysis – In-depth financial insights into bond-issuing companies, helping users assess the creditworthiness and stability of issuers.  
* **Bond Yield Calculator** – A calculator that helps users determine the yield and returns of bonds based on factors like price, coupon rate, and maturity.  
* **Bond Directory** \- Exhaustive list of all the ISIN level data (22k ISIN’s)  
* **Bond Finder** \- The Bond Finder, is a feature that functions as a bond scanner tool. It allows users to explore available bonds, providing information on where each bond can be found and what yields are associated with them.

## **What You Need to Build**

Participants are required to create an **AI layer** that integrates seamlessly with the Tap Bonds platform. The AI layer will consist of:

### **1\. Orchestrator Agent (Main Agent)**

* This agent will manage user queries and assign them to the correct specialized agent based on the context of the prompt.  
* It will compile responses from different agents to provide a structured output to the user.

### **2\. Feature-Specific Agents (4 Agents)**

Each feature will have a dedicated agent responsible for handling queries related to its functionality. The four agents are:

**Bonds Directory Agent**: Provides information on various bonds, including ISIN-level details, credit ratings, maturity dates, and security types.

* **Bond Finder Agent**: Helps users compare bonds across multiple platforms and find the best available yields.  
* **Cash Flow & Maturity Agent**: Handles queries related to bond cash flows, maturity schedules, and payment timelines.

**Bond Screener Agent**

* Performs company-level financial analysis of bond-issuing firms. (analysis of companies already done \- datasets will be provided)  
* Showcase whatever data is available in our screener

**Bond Finder Agent**

* Compares bond yields across various platforms. (currently we have two companies data only)  
* Helps users find the best available investment opportunities available on the finder

**Yield Calculator**

The **Bond Yield Calculator Agent** is designed to help users determine either the **price of a bond based on yield** or the **yield based on price**. It allows investors to make informed decisions by calculating key financial metrics using the bond’s cash flow schedule.

### **How It Works:**

1. **User selects a bond** (by ISIN or issuer name).  
2. **User inputs the investment date** and **number of units** they wish to analyze.  
3. **User chooses what to calculate**:  
   * **If calculating Price** → The user enters the expected yield, and the agent computes the bond price.  
   * **If calculating Yield** → The user enters the bond price, and the agent computes the yield.  
4. **Agent retrieves cash flow details** from the bond directory, including coupon payments, maturity date, and face value.  
5. **The system calculates and returns** the bond's price or yield based on the inputs.

For better understanding we will be linking the excel for how calculator works and its logic

***What are the features? What prompts and responses are expected are linked [here.](https://docs.google.com/document/d/1FizE6-hx7_etW1KLeVWIFB80SXuaz7b73zwS2BvTfDY/edit?usp=sharing)***  
***Read this doc carefully \- to understand what is expected from you.***

##  **Other Requirements**

* **Plug-and-Play**: The agents should work as independent modules that can be integrated easily.  
* **Basic UI Development**: A simple web interface with a **search bar** where users can enter prompts and receive responses.  
* **Efficient Query Handling**: The orchestrator agent should efficiently route queries to the correct agent and compile structured responses.  
* **Demo** : Post deadline there will be a demo call \- to check what has been build.

## **Resources Provided**

* **Database Dump**: Once registered, teams will receive access to a dataset containing bond-related information.  
* **Website Access**: Participants are encouraged to explore [TapBonds.com](https://tapbonds.com) to understand existing features and workflows.  
* **Support from Our Team**: Our team will be available throughout the hackathon weekend for any product guidance.

