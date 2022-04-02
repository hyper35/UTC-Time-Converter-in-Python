import pandas as pd
import numpy as np
import math

def time_converter(year,month,day,second):
    def date_to_jd(year,month,day):
 
        if month == 1 or month == 2:
            yearp = year - 1
            monthp = month + 12
        else:
            yearp = year
            monthp = month

# this checks where we are in relation to October 15, 1582, the beginning of the Gregorian calendar.

        if ((year < 1582) or
            (year == 1582 and month < 10) or
            (year == 1582 and month == 10 and day < 15)):
            
            # before start of Gregorian calendar
            B = 0
        
        else:
            # after start of Gregorian calendar
            A = math.trunc(yearp / 100.)
            B = 2 - A + math.trunc(A / 4.)

        if yearp < 0:
            C = math.trunc((365.25 * yearp) - 0.75)
        
        else:
            C = math.trunc(365.25 * yearp)

        D = math.trunc(30.6001 * (monthp + 1))

        jd = B + C + D + day + 1720994.5

        return jd

    def jd_to_date(jd):
    
        jd = jd + 0.5

        F, I = math.modf(jd)
        I = int(I)

        A = math.trunc((I - 1867216.25)/36524.25)

        if I > 2299160:
            B = I + 1 + A - math.trunc(A / 4.)
        else:
            B = I

        C = B + 1524

        D = math.trunc((C - 122.1) / 365.25)

        E = math.trunc(365.25 * D)

        G = math.trunc((C - E) / 30.6001)

        day = C - E + F - math.trunc(30.6001 * G)

        if G < 13.5:
            month = G - 1
        else:
            month = G - 13

        if month > 2.5:
            year = D - 4716
        else:
            year = D - 4715

        return year, month, day
    
### Dataframe that determines the leap seconds 
    a =[1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0]
    leap_secs = np.array(a).reshape(50,2)


    df = pd.DataFrame(data = leap_secs, index = [1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021], columns = ["Jun 30", "Dec 31"])
    df.index.name = "Year"

### I used this way to handle years, months and days separately
    y = (year - 1971)
    k = df.iloc[:y]

    dec = k["Dec 31"].tolist()
    jun = k["Jun 30"].tolist()

    sum_jun = 0 
    for x in jun: 
        sum_jun = sum_jun + x 

    sum_dec = 0 
    for x in dec: 
        sum_dec = sum_dec + x 

###Determining leap seconds
    while True:
        if 6 < month <12 :
            z = (year - 1972)
            v = df.iloc[:z]
            dec = v["Dec 31"].tolist()

            sum_dec = 0 
            for x in dec: 
                sum_dec = sum_dec + x 

            
            break

        elif month == 6 and day==30:
            z = (year - 1972)
            v = df.iloc[:z]
            dec = v["Dec 31"].tolist()

            sum_dec = 0 
            for x in dec: 
                sum_dec = sum_dec + x 

            
            break

        elif month ==12 and day==31:
            
            break

        elif month < 6:
            z = (year - 1972)
            v = df.iloc[:z]

            dec = v["Dec 31"].tolist()
            jun = v["Jun 30"].tolist()

            sum_jun = 0 
            for x in jun: 
                sum_jun = sum_jun + x 

            sum_dec = 0 
            for x in dec: 
                sum_dec = sum_dec + x
            
            break

### UTC to TAI 
    utc_to_tai = date_to_jd(year, month, day)
    b = utc_to_tai + ((sum_jun + sum_dec) + 10)/86400 + (second/86400)
    
    
    hyper1 = jd_to_date(b)
    
    
    (hyper1[2]*86400)%86400 ##Second of day
    math.floor(hyper1[2]) ##Day
    
    utc_to_tai_output = [hyper1[0],hyper1[1],math.floor(hyper1[2]),(hyper1[2]*86400)%86400]
            

### UTC to TT 
    utc_to_tt = date_to_jd(year, month, day)
    
    a = utc_to_tt + ((sum_jun + sum_dec) + 10 - 32.184)/86400 + (second/86400)
    
    hyper2 = jd_to_date(a)
    
    (hyper2[2]*86400)%86400 ##Second of day
    math.floor(hyper1[2]) ##Day
    
    utc_to_tt_output = [hyper2[0],hyper2[1],math.floor(hyper2[2]),(hyper2[2]*86400)%86400]
    
        
### UTC to GPST
    utc_to_gpst = date_to_jd(year, month, day)
    c = utc_to_gpst + ((sum_jun + sum_dec) - 9)/86400 + (second/86400)
    
    hyper3 = jd_to_date(c)

    
    (hyper3[2]*86400)%86400 ##Second of day
    math.floor(hyper3[2]) ##Day
    
    utc_to_gpst_output = [hyper3[0],hyper3[1],math.floor(hyper3[2]),(hyper3[2]*86400)%86400]
    
    print("TAI: ", utc_to_tai_output)
    print("TT:  ",  utc_to_tt_output)
    print("GPST:",utc_to_gpst_output)