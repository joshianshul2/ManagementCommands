import datetime
import random
from django.core.management.base import BaseCommand
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Sum, Avg
from core.models import User, UserManager, PropertyMaster, Property_TypeMaster, TypeMaster, AvgMaster
import csv
import requests
import schedule
import time
# Scrapper
import requests
import csv
import time
import pdb
import operator
import csv
from django.db.models import F
import random
import re
import pandas as pd
import datetime
import requests
from random import choice
from bs4 import BeautifulSoup
import itertools
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
from selenium.webdriver.firefox.options import Options


class Command(BaseCommand):

    def handle(self, *args, **options):
        # self.get_proxy()
        self.job()

    def job(self):
        k = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.implicitly_wait(5)
        # driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        # options = Options()
        # options.headless = True
        # driver = webdriver.Firefox(options=options)
        status_dict = {1: "Active", 2: "Under Contract", 3: "Off Market", 4: "Sold"}
        df = pd.read_csv('texas_zip_code.csv')
        zipcodelist = df['zip'].tolist()
        # zipcodelist =[75143,75143,75143,75143,75143]
        # zipcodelist= [7583289]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
        }

        try:

            for zip in zipcodelist:
                # Test
                ziptest = PropertyMaster.objects.filter(zip=zip)
                # for p in ziptest:
                #     print("state", p.state)
                # print("TEST", ziptest, "ZIP", zip)
                k += 1
                # for p in ziptest:
                #     print(p.state)

                if len(str(zip)) == 4:
                    zip = "0" + str(zip)
                n = 0
                url = "https://www.landwatch.com/api/property/search/1113/zip-" + \
                      str(zip) + "/land/"
                page = 0
                # print(url)
                # page = requests.get(url, headers=headers)
                if k == 20:
                    k = 0
                    driver.close()
                    driver = webdriver.Chrome(ChromeDriverManager().install())
                    driver.implicitly_wait(5)

                driver.get(url)
                pre = driver.find_element_by_tag_name("pre").text
                data = json.loads(pre)
                print("Start")
                # time.sleep(random.randrange(1, 2))
                print(data['searchResults']['locationSeo']['pageHeaderCount'])
                countListing = data['searchResults']['locationSeo']['pageHeaderCount']
                countListing = re.findall(r'\d+', countListing)
                print(countListing)
                if len(countListing) == 3:
                    page_count = int(int(countListing[2]) / 25 + 2)
                else:
                    page_count = 2
                # print(countListing)

                for i in range(1, page_count):
                    url = "https://www.landwatch.com/api/property/search/1113/zip-" + \
                          str(zip) + "/land/page-" + str(i)
                    # print(url)
                    page = 0
                    driver.get(url)
                    pre = driver.find_element_by_tag_name("pre").text
                    data = json.loads(pre)
                    # print("Length of data : ", data)
                    print("zip", zip)
                    # print(data['searchResults']['propertyResults'])
                    # print(lwPropertyId)
                    # for row in PropertyMaster.objects.all().reverse():
                    #     # print("AJ")
                    #     if PropertyMaster.objects.filter(lwPropertyId=row.lwPropertyId).count() > 1:
                    #         # if PropertyMaster.objects.filter(accountId=row.accountId, acres=row.acres,
                    #         #                                  adTargetingCountyId=row.adTargetingCountyId,
                    #         #                                  address=row.address, baths=row.baths,
                    #         #                                  beds=row.beds, brokerCompany=row.brokerCompany,
                    #         #                                  brokerName=row.brokerName,
                    #         #                                  Url=row.Url,
                    #         #                                  city=row.city,
                    #         #                                  cityID=row.cityID,
                    #         #                                  companyLogoDocumentId=row.companyLogoDocumentId,
                    #         #                                  county=row.county, countyId=row.countyId,
                    #         #                                  description=row.description,
                    #         #                                  hasHouse=row.hasHouse,
                    #         #                                  hasVideo=row.hasVideo,
                    #         #                                  hasVirtualTour=row.hasVirtualTour,
                    #         #                                  imageCount=row.imageCount, zip=row.zip,
                    #         #                                  imageAltTextDisplay=row.imageAltTextDisplay,
                    #         #                                  isHeadlineAd=row.isHeadlineAd,
                    #         #                                  types=' '.join(row.types),
                    #         #                                  isALC=row.isALC,
                    #         #                                  latitude=row.latitude, state=row.state,
                    #         #                                  longitude=row.longitude, price=row.price,
                    #         #                                  status=row.status,
                    #         #                                  Rate=int(row.price / row.acres),
                    #         #                                  ).exists():
                    #             row.delete()
                    #             # print("Good Bye")
                    #         # else:
                    #         #     PropertyMaster.objects.filter(lwPropertyId=row.lwPropertyId).update(
                    #         #         updated_at=datetime.date.today())
                    time.sleep(2)

                    # for p in ziptest:
                    #     print("INSIDER")
                    #     a =p.lwPropertyId
                    #     sum=0
                    #     if a == p.lwPropertyId:
                    #         sum +=1
                    #         print("SUM IS THERE",sum)
                    #     if sum > 1:
                    #         p.delete()
                    #         print("Delete")


                        # if p.lwPropertyId > 1:
                        #     print("Anji")
                        # print(p.state,p.county,p.lwPropertyId,"Hello World")

                    for item in data['searchResults']['propertyResults']:
                        # rate = item['price'] /item['acres']
                        if (item['acres'] == 0):
                            rate = 0

                        else:
                            Rate = item['price'] / item['acres']

                        if item['brokerName'] == "":
                            item['brokerName'] = "NA"

                        prop = PropertyMaster.objects.create(accountId=item['accountId'], acres=item['acres'],
                                                             adTargetingCountyId=item['adTargetingCountyId'],
                                                             address=item['address'], baths=item['baths'],
                                                             beds=item['beds'],
                                                             brokerCompany=item['brokerCompany'],
                                                             brokerName=item['brokerName'],
                                                             Url="https://www.landwatch.com" + item[
                                                                 'canonicalUrl'],
                                                             city=item['city'],
                                                             cityID=item['cityID'],
                                                             companyLogoDocumentId=item[
                                                                 'companyLogoDocumentId'],
                                                             county=item['county'], countyId=item['countyId'],
                                                             description=item['description'],
                                                             hasHouse=item['hasHouse'],
                                                             hasVideo=item['hasVideo'],
                                                             hasVirtualTour=item['hasVirtualTour'],
                                                             imageCount=item['imageCount'], zip=item['zip'],
                                                             imageAltTextDisplay=item['imageAltTextDisplay'],
                                                             isHeadlineAd=item['isHeadlineAd'],
                                                             types=' '.join(item['types']),
                                                             lwPropertyId=item['lwPropertyId'],
                                                             isALC=item['isALC'],
                                                             latitude=item['latitude'], state=item['state'],
                                                             longitude=item['longitude'], price=item['price'],
                                                             status=status_dict[item["status"]],
                                                             Rate=int(Rate)
                                                             )

                print(n, " records found in zipcode : ", zip)
                print("Trial")
                for row in PropertyMaster.objects.filter(zip=zip).reverse():
                    if PropertyMaster.objects.filter(lwPropertyId=row.lwPropertyId).count() > 1:
                        row.delete()
                        print("Ram")

        finally:
            driver.close()
            print("Completed")
