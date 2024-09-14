#ifndef USER_CODE_H
#define USER_CODE_H

#include <vector>
#include <string>
#include <utility>
#include <iostream>
#include <algorithm>
#include "fileIterator.h"
#include "fileWriter.h"
#include <sstream> 
#include <unordered_set>

using namespace std;



// #PROMPT# Split function to split a line into tokens. Use this function to split the lines read from the files.
    vector<string> split(const string& line, char delimiter) {
        vector<string> tokens;
        stringstream ss(line);
        string token;
        while (getline(ss, token, delimiter)) {
            tokens.push_back(token);
        }
        return tokens;
    }

//////////////////////////////////////////////////////////////////////////////////
// MODIFY THIS SECTION
//////////////////////////////////////////////////////////////////////////////////
/**
 * @brief Modify this code to solve the assigment. Include relevant document. Mention the prompts used prefixed by #PROMPT#.
 *        
 * 
 * @param hashtags 
 * @param purchases 
 * @param prices 
 */
void groupCustomersByHashtags(fileIterator& hashtags, fileIterator& purchases,fileIterator& prices, int k, string outputFilePath)
{
    //Use this to log compute time    
    auto start = high_resolution_clock::now();
    
    /*
    #PROMPT# Read the hashtags data using the hashtags file iterator and store it in a suitable data structure.
    */

    unordered_map<int, vector<string>> hashtagsMap;
    while (hashtags.hasNext()) {
        string line = hashtags.next();
        if (line.empty()) break;
        vector<string> tokens = split(line, ',');
        int product_id = stoi(tokens[0]);
        vector<string> hashtags(tokens.begin() + 1, tokens.end());
        hashtagsMap[product_id] = hashtags;
    }

    // // Debug
    // for (auto it = hashtagsMap.begin(); it != hashtagsMap.end(); it++) {
    //     cout << it->first << " ";
    //     for (auto tag : it->second) {
    //         cout << tag << " ";
    //     }
    //     cout << endl;
    // }

    /*
    #PROMPT# Create an unordered_map<int, unordered_map<string, int>> to store the count
     of hashtags for each customer. Read from the purchases file iterator and update the count.
    */
    unordered_map<int, unordered_map<string, int>> hashtagCount;
    while (purchases.hasNext()) {
        string line = purchases.next();
        if (line.empty()) break;
        vector<string> tokens = split(line, ',');
        int customer_id = stoi(tokens[0]);
        int product_id = stoi(tokens[1]);
        if (hashtagsMap.find(product_id) != hashtagsMap.end()) {
            for (auto hashtag : hashtagsMap[product_id]) {
                hashtagCount[customer_id][hashtag]++;
            }
        }
    }

    // // Debug
    // for (auto it = hashtagCount.begin(); it != hashtagCount.end(); it++) {
    //     cout << it->first << ":";
    //     for (auto tag : it->second) {
    //         cout << tag.first << " " << tag.second << " ";
    //     }
    //     cout << endl;
    // }

    /*
    #PROMPT# unordered_map<int, vector<string>> customerPrimaryInterests  Determine primary interests.
    Sort in descending order of frequency and then second level ascending lexographical order.
    */
    unordered_map<int, vector<string>> customerPrimaryInterests;
    for (auto it = hashtagCount.begin(); it != hashtagCount.end(); it++) {
        vector<pair<string, int>> tags(it->second.begin(), it->second.end());
        sort(tags.begin(), tags.end(), [](const pair<string, int>& a, const pair<string, int>& b) {
            if (a.second == b.second) {
                return a.first < b.first;
            }
            return a.second > b.second;
        });
        vector<string> primaryInterests;
        for (int i = 0; i < k && i < tags.size(); i++) {
            primaryInterests.push_back(tags[i].first);
        }
        customerPrimaryInterests[it->first] = primaryInterests;
    }

    // // Debug
    // for (auto it = customerPrimaryInterests.begin(); it != customerPrimaryInterests.end(); it++) {
    //     cout << it->first << ":";
    //     for (auto tag : it->second) {
    //         cout << tag << " ";
    //     }
    //     cout << endl;
    // }

    /*
    #PROMPT# Determine the interest groups based on primary interests. If two customers have same elements 
    in customerPrimaryInterests.second in any order, they are in the same group.
    */

    unordered_map<string, vector<int>> groupMap;
    for (auto it = customerPrimaryInterests.begin(); it != customerPrimaryInterests.end(); it++) {
        vector<string> primaryInterests = it->second;
        sort(primaryInterests.begin(), primaryInterests.end());
        string key = "";
        for (auto tag : primaryInterests) {
            key += tag + ",";
        }
        groupMap[key].push_back(it->first);
    }

    // // Debug
    // for (auto it = groupMap.begin(); it != groupMap.end(); it++) {
    //     cout << it->first << ":";
    //     for (auto customer : it->second) {
    //         cout << customer << " ";
    //     }
    //     cout << endl;
    // }
    

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    cout << "Time taken by compute part of the function: "<< duration.count() << " microseconds" << endl;

    // Use the below utility function to write the output to a file
    // Call this function for every group as a vector of integers
    for(auto it = groupMap.begin(); it != groupMap.end(); it++){
        vector<int> group = it->second;
        writeOutputToFile(group, outputFilePath);
    }
    return;
}

//////////////////////////////////////////////////////////////////////////////////
// MODIFY THIS SECTION
//////////////////////////////////////////////////////////////////////////////////
/**
 * @brief Modify this code to solve the assigment. Include relevant document. Mention the prompts used prefixed by #PROMPT#.
 *        
 * 
 * @param customerList 
 * @param purchases 
 * @param prices
 */
float calculateGroupAverageExpense(vector<int> customerList, fileIterator& purchases,fileIterator& prices){
    //Use this to log compute time    
    auto start = high_resolution_clock::now();
    
    /*
    #PROMPT# Read the prices data using the prices file iterator and store it in a suitable data structure. 
    We want O(1) access and insert to the prices of items. Use a hashMap named pricesMap to store the prices of items.
    */

    unordered_map<int, float> pricesMap;
    while (prices.hasNext()) {
        string line = prices.next();
        if (line.empty()) break;
        vector<string> tokens = split(line, ',');
        int product_id = stoi(tokens[0]);
        float price = stof(tokens[1]);
        pricesMap[product_id] = price;
    }

    // // Debug
    // for (auto it = pricesMap.begin(); it != pricesMap.end(); it++) {
    //     cout << it->first << " " << it->second << endl;
    // }


    /*
    #PROMPT# Store the customerList in a suitable data structure so that checking whether a customer is in the group is O(1).
    */
    unordered_set<int> customerSet(customerList.begin(), customerList.end());

    // // Debug
    // for (auto customer : customerList) {
    //     cout << customer << " ";
    // }
    // cout << endl;

    /*
    #PROMPT# Read the purchases data using the purchases file iterator and calculate the total expense of the group.
    */
    float totalExpense = 0.0;
    float groupSize = 1.0*customerList.size();

    while (purchases.hasNext()) {
        string line = purchases.next();
        if (line.empty()) break;
        vector<string> tokens = split(line, ',');
        int customer_id = stoi(tokens[0]);
        int product_id = stoi(tokens[1]);
        if (customerSet.find(customer_id) != customerSet.end()) {
            totalExpense += pricesMap[product_id];
        }
    }

    float avgExpense = totalExpense / groupSize;

    // // Debug
    // cout << "Total expense: " << totalExpense << endl;
    // cout << "Group size: " << groupSize << endl;
    // cout << "Average expense: " << avgExpense << endl;
    

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    cout << "Time taken by this function: "<< duration.count() << " microseconds" << endl;

    return avgExpense;
}


//////////////////////////////////////////////////////////////////////////////////
// MODIFY THIS SECTION
//////////////////////////////////////////////////////////////////////////////////
/**
 * @brief Modify this code to solve the assigment. Include relevant document. Mention the prompts used prefixed by #PROMPT#.
 *        
 * 
 * @param hashtags 
 * @param purchases 
 * @param prices
 * @param newHashtags
 * @param k
 * @param outputFilePath
 */
void groupCustomersByHashtagsForDynamicInserts(fileIterator& hashtags, fileIterator& purchases,fileIterator& prices,vector<string> newHashtags, int k, string outputFilePath){
    //Use this to log compute time    
    auto start = high_resolution_clock::now();
    //  Write your code here
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    cout << "Time taken by compute part of the function: "<< duration.count() << " microseconds" << endl;

    // Use the below utility function to write the output to a file
    // Call this function for every group as a vector of integers
    vector<int> group;
    writeOutputToFile(group, outputFilePath);
    return;
    
}



#endif // USER_CODE_H
