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
from apscheduler.schedulers.background import BackgroundScheduler
# Scrapper
import requests
import csv
import time
import pdb
import operator
import  csv
from django.db.models import F
import random
import re

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.job2()

    def job2(self):
        status_dict = {1: "Active", 2: "Under Contract", 3: "Off Market", 4: "Sold"}
        # a=0
        print("Anji...")
        print("I'm Ram...")
    
        with open('zip_code_database.csv', 'r') as file:
            # head = [next(myfile) for x in range(N)]
                reader = csv.reader(file)
            # for row in reader:
        #         print(row)
        # zipcode_list = [75002, 75006, 75007, 75009, 75010, 75013, 75019, 75020, 75021, 75022, 75024, 75028, 75032,
        #                 75034, 75035, 75038, 75040, 75041, 75043, 75044, 75048, 75050, 75051, 75056, 75057, 75058,
        #                 75061, 75063, 75065, 75067, 75068, 75069, 75070, 75071, 75074,75076, 75077, 75078, 75080, 75081, 75083, 75087, 75088, 75089, 75090, 75092, 75093, 75097, 75098, 75102, 75103, 75104, 75105, 75109, 75110, 75114, 75115, 75116, 75117, 75119, 75124, 75126, 75135, 75142, 75143, 75144, 75147, 75148, 75154, 75156, 75159, 75160]

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                    "Accept-Encoding": "*",
                    "Connection": "keep-alive"
                }
                try:

                    for zip in reader:
                        if len(str(zip)) == 4:
                            zip = "0" + str(zip)
                        n = 0
                        url = "https://www.landwatch.com/api/property/search/1113/zip-" + \
                            str(zip) + "/land/listed-1-day"
                        page = 0
                        # print(url)
                        page = requests.get(url, headers=headers)
                        # time.sleep(random.randrange(1, 2))
                        while (page == 0):
                            page = requests.get(url, headers=headers)
                            time.sleep(random.randrange(1, 5))
                        data = page.json()
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
                                str(zip) + "/land/listed-1-day/page-" + str(i)
                            # print(url)
                            page = 0
                            page = requests.get(url, headers=headers)
                            # time.sleep(random.randrange(1, 2))
                            while (page == 0):
                                page = requests.get(url, headers=headers)
                                time.sleep(random.randrange(1, 5))
                            data = page.json()
                            # print("Length of data : ",len(data))

                            for item in data['searchResults']['propertyResults']:
                                # a=a+1
                                print(item['zip'][0])
                                prop = PropertyMaster.objects.create(accountId=item['accountId'], acres=item['acres'],
                                                                    adTargetingCountyId=item['adTargetingCountyId'],
                                                                    address=item['address'], baths=item['baths'],
                                                                    beds=item['beds'], brokerCompany=item['brokerCompany'],
                                                                    brokerName=item['brokerName'],
                                                                    Url="https://www.landwatch.com" + item['canonicalUrl'],
                                                                    city=item['city'],
                                                                    cityID=item['cityID'],types=''.join(item['types']),
                                                                    companyLogoDocumentId=item['companyLogoDocumentId'],
                                                                    county=item['county'], countyId=item['countyId'],
                                                                    description=item['description'], hasHouse=item['hasHouse'],
                                                                    hasVideo=item['hasVideo'],
                                                                    hasVirtualTour=item['hasVirtualTour'],
                                                                    imageCount=item['imageCount'],
                                                                    imageAltTextDisplay=item['imageAltTextDisplay'],
                                                                    isHeadlineAd=item['isHeadlineAd'],
                                                                    lwPropertyId=item['lwPropertyId'], isALC=item['isALC'],
                                                                    latitude=item['latitude'], state=item['state'],
                                                                    longitude=item['longitude'], price=item['price'],
                                                                    Rate=item['price'] / item['acres'], status=status_dict[item["status"]],
                                                                    zip=item['zip'],

                                                                    )

                                ###do something###

                                n = n + 1
                            print("n=",n)

                            # for item in data['searchResults']['propertyResults']:
                            #     if PropertyMaster.objects.filter(lwPropertyId=item['lwPropertyId']).exists():
                            #
                            #         if PropertyMaster.objects.all().values().filter(lwPropertyId=item[lwPropertyId],
                            #                                                         user=request.user):
                            #             PropertyMaster.objects.all().values().filter(lwPropertyId=item[lwPropertyId],
                            #                                                          user=request.user).update(
                            #                 accountId=item['accountId'], acres=item['acres'],
                            #                 adTargetingCountyId=item['adTargetingCountyId'],
                            #                 address=item['address'], baths=item['baths'],
                            #                 beds=item['beds'], brokerCompany=item['brokerCompany'],
                            #                 brokerName=item['brokerName'],
                            #                 Url="https://www.landwatch.com" + item['canonicalUrl'],
                            #                 city=item['city'],
                            #                 cityID=item['cityID'],
                            #                 companyLogoDocumentId=item['companyLogoDocumentId'],
                            #                 county=item['county'], countyId=item['countyId'],
                            #                 description=item['description'], hasHouse=item['hasHouse'],
                            #                 hasVideo=item['hasVideo'],
                            #                 hasVirtualTour=item['hasVirtualTour'],
                            #                 imageCount=item['imageCount'],
                            #                 imageAltTextDisplay=item['imageAltTextDisplay'],
                            #                 isHeadlineAd=item['isHeadlineAd'],
                            #                 lwPropertyId=item['lwPropertyId'], isALC=item['isALC'],
                            #                 latitude=item['latitude'], state=item['state'],
                            #                 longitude=item['longitude'], price=item['price'],
                            #                 Rate=item['price'] / item['acres'], status=item['status'], zip=item['zip'],
                            #
                            #             )
                            #             print("1")
                            #         else:
                            #             mylist_obj = PropertyMaster.objects.all().values().filter(lwPropertyId=item[lwPropertyId],
                            #                                                                       user=request.user).update(
                            #                 accountId=item['accountId'], acres=item['acres'],
                            #                 adTargetingCountyId=item['adTargetingCountyId'],
                            #                 address=item['address'], baths=item['baths'],
                            #                 beds=item['beds'], brokerCompany=item['brokerCompany'],
                            #                 brokerName=item['brokerName'],
                            #                 Url="https://www.landwatch.com" + item['canonicalUrl'],
                            #                 city=item['city'],
                            #                 cityID=item['cityID'],
                            #                 companyLogoDocumentId=item['companyLogoDocumentId'],
                            #                 county=item['county'], countyId=item['countyId'],
                            #                 description=item['description'], hasHouse=item['hasHouse'],
                            #                 hasVideo=item['hasVideo'],
                            #                 hasVirtualTour=item['hasVirtualTour'],
                            #                 imageCount=item['imageCount'],
                            #                 imageAltTextDisplay=item['imageAltTextDisplay'],
                            #                 isHeadlineAd=item['isHeadlineAd'],
                            #                 lwPropertyId=item['lwPropertyId'], isALC=item['isALC'],
                            #                 latitude=item['latitude'], state=item['state'],
                            #                 longitude=item['longitude'], price=item['price'],
                            #                 Rate=item['price'] / item['acres'],status=status_dict[item["status"]], zip=item['zip'],
                            #
                            #             )
                            #             print("2")
                            #             mylist_obj.save()
                            #     else:
                            #         print("Aj")
                            #         # PropertyMaster.objects.filter(id=item[lwPropertyId]).delete()
                            #         PropertyMaster.save()
                            #     # entry = TypeMaster.objects.all()
                        print(n, " records found in zipcode : ", zip)

                finally:
                    print("Completed")
        return True
