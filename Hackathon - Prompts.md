1A Bonds Directory is a structured database containing details of various bonds available in the market. It provides ISIN-level information for thousands of bonds, allowing users to search, filter, and analyze bonds based on multiple criteria like issuer, coupon rate, maturity date, credit rating, security type, and listing details. This directory serves as a centralized knowledge hub, helping investors make informed decisions by providing accurate, up-to-date bond data sourced from public financial datasets.

### **1️⃣ Basic ISIN Lookup**

**Prompt:** "Show me details for ISIN INE123456789"

✅ **Key pointers in the expected response:**

* **Issuer Name:** XYZ Capital Ltd.  
* **Type of Issuer:** Non-PSU  
* **Sector:** Financial Services  
* **Coupon Rate:** 10.5%  
* **Instrument Name:** 10.5% XYZ Secured NCDs  
* **Face Value:** ₹1,00,000  
* **Total Issue Size:** ₹50 Cr  
* **Redemption Date:** 15-06-2028  
* **Credit Rating:** AA (Stable) by CRISIL  
* **Listing Details:** NSE, Listed on 20-01-2024  
* **Key Documents:** \[Offer Document PDF\], \[Trust Deed PDF\]

**Prompt:** "Show me all the issuances done by Ugro Capital."

✅ **Key pointers in the expected response:**

* **Ugro Capital Private Limited has issued 13 bonds in total.**  
* **10 have matured, and 3 are active.**  
* **Table of ISINs:**

| ISIN | Coupon Rate | Maturity Date | Face Value | Credit Rating | Issuance Size |
| ----- | ----- | ----- | ----- | ----- | ----- |
| INE123456789 | 9.2% | 10-12-2027 | ₹1,00,000 | AAA | 25cr |
| INE987654321 | 10.0% | 05-09-2030 | ₹10,00,000 | AA+ | 45cr |

### **2️⃣ Filter-Based Search**

**Prompt:** "Find me secured debentures with a coupon rate above 10% and maturity after 2026."

✅ **Key pointers in the expected response:**

**There are (give number) of bonds which fit the criteria, and list out details of few.**

* **ISIN:** INE765432109  
* **Issuer:** ABC Finance  
* **Coupon Rate:** 10.75%  
* **Redemption Date:** 15-09-2028  
* **Security:** Secured

### **3️⃣ Credit Rating-Specific Query**

**Prompt:** "Show all bonds rated AA+ or higher issued by financial institutions."

✅ **Key pointers in the expected response:**

* **There are around 1500 bonds with AA+ or higher rating.**  
* **Preview of 30 bonds (ISIN, issuer, coupon, maturity).**  
* **Option to show more.**

### **4️⃣ Maturity Date Lookup**

**Prompt:** "Which bonds are maturing in 2025?"

✅ **Expected Response:**

* **List of ISINs, issuer names, and maturity dates.**  
* **Option to download tabular data of this**

### **5️⃣ Cash Flow Schedule Inquiry**

**Prompt:** "Show me the cash flow schedule for ISIN INE567890123."

✅ **Key pointers in the expected response:**

| Date | Type |  |
| :---- | :---- | :---- |
| 10-06-2024 | Interest Payment |  |
| 10-12-2024 | Interest Payment |  |
| 10-06-2025 | Interest Payment |  |
| 10-12-2025 | Principal \+ Interest |  |

### **6️⃣ Bond Security Details Inquiry**

**Prompt:** "What are the security details for \[ISIN\] INE789012345?"

✅ **Key pointers in the expected response:**

* **Security Type:** Secured  
* **Asset Coverage:** Principal \+ Interest  
* **Coverage Ratio:** 120%  
* **Security Measures:** First charge over fixed assets worth ₹200 Cr

### **7️⃣ Document Retrieval**

**Prompt:** "Help me with the document for ISIN INE678901234."

✅ **Expected Response:**

* **Brief summary of the contents of document**  
* **\[Download Offer Document\] button**

**Prompt:** "Help me with the documents for Akara Capitals?"

✅**Key pointers in the expected response:**

* **List of ISINs issued by Akara Capital.**  
* **User selects the ISIN to retrieve the document.**

### **8️⃣ Debenture Trustee Inquiry**

**Prompt:** "Who is the debenture trustee for ISIN INE890123456?"

✅ **Expected Response:**

* **Trustee Name:** Beacon Trusteeship Pvt. Ltd.

### **9️⃣ Listing Exchange & Trading Status**

**Prompt:** "Where is ISIN INE901234567 listed, and is it actively traded?"

✅ **Expected Response:**

* **Listing Exchange:** BSE & NSE  
* **Listing Date:** 05-08-2023  
* **Trading Status:** Active

### **🔟 Face Value Inquiry**

**Prompt:** "What is the face value of ISIN INE567890123 Ugro Capital bond?"

✅ **Expected Response:**

* **Face Value:** ₹1,00,000  
* **Error Handling:** "The given ISIN does not belong to Ugro Capital. It is associated with Reliance Industries."

**Proper responses need to be there**  
Error handling \- 

If user searches ISIN and company name in same prompt and they don’t match?  
Example: Handle \- ISIN does not belong to given company name. ISIN belongs to XYZ company and company ABC has these 10 ISINs and list these ISINs

All the data would be available in the bonds directory sections

Directory Link: [https://tapbonds.com/directory](https://tapbonds.com/directory)

## **Bond Finder**

A **Bond Finder** is a discovery tool designed to help investors look for a bond and compare it across multiple platforms. Similar to how travel aggregators like Skyscanner function for flights, Bond Finder aggregates bond listings from different partner platforms like **SMEST** and **FixedIncome**.  
(only tied up with above 2 companies)

It provides investors with essential bond details, including **issuer name, ISINs, credit rating, yield range, maturity date, and availability across platforms**. This enables users to **identify the best yield, compare bond options, and decide where to purchase a bond at the most favorable terms**.

### **1️⃣ General Inquiry**

**Prompt:** "Show me what all bonds are available in the bond finder."

✅ **Expected Response:**

* **Currently showcasing bonds available on SMEST and FixedIncome.**  
* **Sample bonds:**

| Issuer | Rating | Yield |  | Available at |
| :---- | :---- | :---- | :---- | :---- |
| Tata Capital | AAA | 7.5%-8.0% |  | SMEST |
| Indiabulls Housing Finance | AA | 9.2%-9.8% |  | FixedIncome & SMEST |

---

### **2️⃣ Platform Availability**

**Prompt:** "Where can I buy bonds from XYZ issuer?"

✅ **Expected Response:**

* **XYZ Ltd bonds available on FixedIncome with a yield range of 8.5%-9.1%.**  
* **Error Handling:** "Bonds from XYZ Ltd are currently not available."

### **3️⃣ Yield-Based Search**

**Prompt:** "List all bonds available with a yield of more than 9%."

✅ **Expected Response:**

| Issuer | Rating | Yield |  | Available at |
| :---- | :---- | :---- | :---- | :---- |
| Piramal Capital | A | 9.5%-10.1% |  | SMEST |
| Shriram Finance | AA | 9.3%-9.9% |  | FixedIncome |

**Users can search for yield, face value, min investment**

### **4️⃣ Best Yield Comparison**

**Prompt:** "Which platform has the best yield for 5-year bonds?"

✅ **Expected Response:**

* **FixedIncome offers the highest yield at 9.2% for 5-year bonds.**

### **5️⃣ Credit Rating-Based Search**

**Prompt:** "List bonds with a rating of A or lower."

✅ **Expected Response:**

| Issuer | Rating | Yield | Maturity | Available at |
| :---- | :---- | :---- | :---- | :---- |
| XYZ Capital | A | 10.2%-10.8% | 2026 | FixedIncome  |

Bond Finder : [https://tapbonds.com/finder](https://tapbonds.com/finder)

These are the sample prompts and answers expected from the model. 

### **1.0. What is the Bond Screener on Tap Bonds?**

The Bond Screener is a tool provided by Tap Bonds that allows investors to evaluate bond-issuing companies by analyzing key trends, financial ratios, and the latest news, enabling informed investment decisions.

### **2.0. How can I access the Bond Screener?**

To access the Bond Screener, navigate to the 'Tools' section on the Tap Bonds website and select 'Bond Screener'. You may need to sign in or create an account to use this feature at full potential.

### **3.0. What information can I analyze using the Bond Screener?**

The Bond Screener allows you to analyze key trends, financial ratios, and the latest news related to bond-issuing companies, helping you make informed investment decisions.

### **4.0. Is there a cost associated with using the Bond Screener?**

The information available does not specify whether there is a cost associated with using the Bond Screener. For detailed information, please visit the Tap Bonds website or contact their support team.

### **5.0. Can I use the Bond Screener to compare different bonds?**

Yes, the Bond Screener is designed to help you evaluate and compare different bonds by providing detailed analyses of bond-issuing companies.

### **6.0. Do I need an account to use the Bond Screener?**

Accessing the Bond Screener may require you to sign in or create an account on the Tap Bonds platform.

### **7.0. How frequently is the information in the Bond Screener updated?**

The information available does not specify the update frequency of the Bond Screener data. For detailed information, please visit the Tap Bonds website or contact their support team.

### **8.0. Can I save my screening criteria for future use?**

The information available does not specify whether you can save your screening criteria. For detailed information, please visit the Tap Bonds website or contact their support team.

### **9.0. Is the Bond Screener suitable for beginners?**

The Bond Screener is designed to assist investors in evaluating bond-issuing companies. If you're new to bond investing, you may also consider using the 'Talk to Expert' feature on Tap Bonds for personalized guidance.

### **10.0. Where can I find more information or assistance regarding the Bond Screener?**

For more information or assistance, you can visit the 'Knowledge Centre' on the Tap Bonds website, which includes FAQs and other resources, or use the 'Talk to Expert' feature for personalized support.

### **11.0. How many companies are there in Bond Screener?**

Count from the list of companies in bond screener

### **12.0. What is the rating of ABC company?**

Fetch from table

### **13.0. ABC company is in which sector?**

Fetch from table

### **14.0. ABC company is in which industry?**

Fetch from table

### **15.0. Give me a summary about ABC company**

Generate AI summary

### **16.0. What is the EPS of ABC company?**

Fetch from Key metrics

### **17.0. What is the current ratio of ABC company?**

Fetch from Key metrics

### **18.0. What is the Debt/Equity of ABC company?**

Fetch from Key metrics

### **19.0. What is the Debt/EBITDA of ABC company?**

Fetch from Key metrics

### **20.0. What is the interest coverage ratio of ABC company?**

Fetch from Key metrics

### **21.0. What is the operating cashflow to total Debt of ABC company?**

Fetch from Key metrics

### **22.0. Compare X ratio/metric of ABC company with DEF company.**

Provide in text/tabular and inform which one has better metric?

### **23.0. What is the {Specicific financial metric} of ABC company?**

Fetch from Financials

### **24.0. What is the growth rate of {Specific Financial Metric} of ABC company.**

nan

### **25.0. What are the PROS and CONS of ABC company?**

Fetch from Pros and cons section of a company page.

### **26.0. List of lenders of ABC limited.**

Fetch from lenders section of a company page.

### **27.0. Top lenders of ABC limited**

Fetch from lenders section of a company page.

### **28.0. List of ISINs under ABC limited**

Fetch from isin section of a company page.

### **29.0. Recent news/events/article/blog about ABC company**

Fetch from news section of screener page, blogs from Knowledge centre.

###  

## **Calculator**

### **30\. How can I calculate clean price of a bond?**

ask them to use calculator from tool or ask for parameters to fill and calculate results.

### **31\. How can I calculate consideration of a bond?**

ask them to use calculator from tool or ask for parameters to fill and calculate results.

### **32\. What will be the consideration for {ISIN} for {units} at {date}?**

ask them to use calculator from tool or ask for parameters to fill and calculate results.

### **33\. Price to yield calculation**

Calculate from calculator tool and generate result.

—

For understanding how the calculator works  
We are attaching an sample excel here with formulas and logic   
**Attached File :** [INE08XP07258\_28-Feb-2025\_Cashflow](https://docs.google.com/spreadsheets/d/1TX0GfILVfdyJKIwwqvBNhDi5Qmu94cdqgW9mc2op9po/edit?usp=sharing)

