import numpy_financial as npf
import numpy as np
import datetime as dt
import calendar
import pandas as pd
#-------------------------------------------------------------------------
#this python code will be written so that the first section will contian functions pertaining to the dirty price, clean price, and fractional periods.
#the second section will use the functions from the first section to calculate the HPY, RCY. Additionally, it will calulate the modified duration, DV01, etc.

#-------------------------------------------------------------------------
#need to create a class in python. This can either give you the clean price or the dirty price, which is more commonly used.
#for the nper, the clean price does not include the previous coupon payment, so its the actual nper. 

    last_coupon_date_presettle = dt.date(2023,2,15)
    first_coupon_date_postsettle = dt.date(2023,8,15)
    settlement_date = dt.date(2023, 3, 7)

    # yield_ = 0.03959654
    # face_value = 100
    # period = 19
    # coupon_percentage = 0.035
    # coupon_payment = coupon_percentage * face_value
    
class treasury_price(yield_, coupon, face_value, nper, last_coupon_date, first_coupon_date, settlement_date, type_of_price):
   
    #clean = 0, dirty = 1
    clean_or_dirty = type_of_price
    last_coupon_date_presettle = last_coupon_date
    first_coupon_date_postsettle = first_coupon_date
    settlement_date = settlement_date
    coupon_payment = coupon * face_value
    
    #use the street convention for the yield as it will give you a more accurate price for the dirty price of the bond.
    #street convention means that bond payments are made on the date scheduled, regardless of holidays.
    dirty_price = calculate_dirty_price(coupon_percentage, yield_, 20, face_value, fractional_per)
    acc_int = accrued_interest(fractional_per, coupon_payment)
    clean_price = dirty_price - round(acc_int,20)
    #in the future, possibly need a 30/360 day count convention.

    def actual_actual(start_date, end_date, settle):
        #days remaining - number of days between the settlement and coupon.
        days_remaining = end_date - settle
        #the basis is the days between the coupon dates - this is the main difference between the date conventions.
        basis = end_date - start_date
        #the fractional period is used to subtract from the n in bond pricing - this amount is given to the buyer of the bond.
        fractional_period = days_remaining/basis
        return fractional_period

  
    fractional_per = actual_actual(last_coupon_date_presettle, first_coupon_date_postsettle, settlement_date)
    print(fractional_per, 'this is the fractional period')

    #do not add the fracitonal period if we are calculating the clean price
    def calculate_dirty_price(coupon_rate, ytm, time, FV, fractional_period=1):
        ytm1 = ytm/2
        face_value = FV
        coupon = (coupon_rate/2)*FV
        #c/y
        coupon_yield = coupon/ytm1
        #(1+y)^t-1
        compounding_yield = ((1+ytm1)**(time*2))-1
        #(C/y)((1+y)^t-1))+FV
        total_future_CF = (coupon_yield*compounding_yield)+face_value 
        #adjusted time left for compounding
        adjusted_time = (time*2) - (1-fractional_period)
        discount = (1+ytm1)**adjusted_time
        #total future cash flows divided by the discounting factor to get the dirty price.
        dirty_price = total_future_CF/discount
        
        return dirty_price
        
    def accrued_interest(fractional_period, coupon):
        coupon_semi = coupon/2
        stub = 1-fractional_period
        stub_coupon = stub*coupon_semi
        print(stub_coupon)
        return stub_coupon
        
    #-----------------------------------------------------------------------------------------------------------------------

    # DCF = pd.DataFrame()
    # print(DCF)

    # #TODO: if you want to see the full dataset of the cash flow reinvestments
    # def calculate_future_cash_flows(coupon, reinvestment_rate, discount_period, periods):
        # pass

    #this has to do with the holding period yield. We need both the coupons to determine the period of compounding for the future value. 
    maturity_date = dt.date(2033,2,15)
    first_coupon = dt.date(2023,8,15) 
    last_coupon = dt.date(2023,2,15)

    coupon_pre_sold1 = dt.date(2023,2,15) 
    coupon_post_sold1 = dt.date(2023,8,15)

    Bond_FV = 0
    #this is the amount of years that the coupon or reinvestment will be compounded for.
    compounding_periods = 0
    discounting_periods = 0
    def coupon_number(maturity, coupon1, coupon2, coupon_pre_sold, coupon_post_sold):
        fractional = actual_actual(coupon_post_sold1, coupon_pre_sold1, maturity)
        periods = 0
        coupon_date1 = coupon1
        coupon_date2 = coupon2
        #this function is to calculate how many periods you need to 
        while True:
            if (periods % 2) == 0 and coupon_date1 < maturity:
                periods += 1
                next_coupon1 = coupon_date1.replace(year=coupon_date1.year + 1)
                coupon_date1 = next_coupon1
                
            if (periods % 2) != 0 and coupon_date2 < maturity:
                periods += 1
                next_coupon2 = coupon_date2.replace(year=coupon_date2.year + 1)
                coupon_date2 = next_coupon2
                
            if coupon_date1 > maturity:
                break
        
        compounding_periods = periods-2
        discounting_periods = periods-2+fractional
        print(compounding_periods)
        print(discounting_periods)
        
    def future_value(present_value, interest_rate, discount_period):
        semi_annual_rate = (interest_rate/2)/100
        FV = present_value*(1+semi_annual_rate)**(discount_period)
        Bond_FV = FV
        #missing present_value
        
    # coupon_number(maturity_date, first_coupon, last_coupon, coupon_pre_sold1, coupon_post_sold1)
    # Bond_FV = future_value(dirty_price, 3.499766, discounting_periods)
    # print(Bond_FV)
    
    #---------------------------------------------------------------------------------------------------------------
    #The holding period yield (HPY) is the yield or amount made after holding the bond for a certain period of time. The PV is the price that was bought, the FV is the price that was sold.
    #The present value in this case is the dirty price of the bond. 
    
    #------------------------------------------------------------------------------------------------------------------
    #DV01 (Actual Price Changes, both prices resulting from changes in the interest rates need to be shown)
    #Thought: Since bonds are quoted in the clean price, need to give the price change in the clean price.

    settlement_date = 3/6/2023
    maturity = 2/15/2033

    bp = 200
    temp_clean_price= calculate_dirty_price(coupon_percentage, yield_, 20, face_value, fractional_per)
    print(temp_clean_price, 'this is the temp dirty price')

    bp_adjustment = bp*(1/10000)
    #need to set the basis point, bp is 1/100 of 1/100 of 1.
    print(yield_, 'this is the yield')

    #adjusted yields
    yield_add_bp = yield_+bp_adjustment
    yield_subtract_bp = yield_-bp_adjustment
    print(yield_subtract_bp, 'this is the yield subtracted by 20 bps')

    print(yield_add_bp, yield_subtract_bp, 'these are the yields')

    dirty_price_half_up = calculate_dirty_price(coupon_percentage, yield_add_bp, 20, face_value, fractional_per)
    dirty_price_half_down = calculate_dirty_price(coupon_percentage, yield_subtract_bp, 20, face_value, fractional_per)

    print(dirty_price_half_up, dirty_price_half_down)

    #----------------------------------------------------------------------------------------------------
    #This section calculates the DV01/convexity in python.
    yield_half_up = yield_+0.00005
    yield_half_down = yield_-0.00005

    print(yield_half_up, yield_half_down, 'yields')

    dirty_price_half_basis_up = calculate_dirty_price(coupon_percentage, yield_half_up, 20, face_value, fractional_per)
    dirty_price_half_basis_down = calculate_dirty_price(coupon_percentage, yield_half_down, 20, face_value, fractional_per)

    print(dirty_price_half_basis_up, dirty_price_half_basis_down, 'dirty price')

    #convexity 
    P_Rise = dirty_price_half_up
    P_Fall = dirty_price_half_down

    #-2p0
    double_initial = -2*temp_clean_price
    initial = temp_clean_price
    change_in_y_squared= bp_adjustment**2
    top_added=P_Rise+P_Fall+double_initial
    bottom_added=initial*change_in_y_squared
    Convexity=top_added/bottom_added
    Convexity_adjustment = (Convexity/2)*initial*(bp_adjustment**2)

    print(Convexity, Convexity_adjustment)

    change_in_price_up = temp_clean_price - dirty_price_half_basis_up
    change_in_price_down = dirty_price_half_basis_down - temp_clean_price 

    print(change_in_price_up, change_in_price_down)

    DVO1 = change_in_price_up+change_in_price_down
    print(DVO1)
    dollar_duration = DVO1 * 10000
    print(dollar_duration)
    modified_duration = dollar_duration/temp_clean_price
    print(modified_duration)

treasury_price(str(clean), 0.03959654, 0.035, 100, 20, dt.date(2023,2,15), dt.date(2023,8,15), dt.date(2023, 3, 7), 1)
