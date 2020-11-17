import datetime
from accounts.models import User
from django.utils import timezone
from wallets.models import Wallet
from datetime import timedelta, date
from referrals.models import Referral, Link
from .serializers import ReferralSerializer
from KazubamarketApi.permissions import IsActivatedUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView

########## REFERRAL DETAIK API VIEW ##########    
class ReferralAPIView(ListAPIView):
    """
    Endpoint for Referral Detail, viewed by Activated.
    """
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    serializer_class = ReferralSerializer
    permission_classes = [IsActivatedUser]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        query_view = int(pk)
        user = self.request.user
        first_generation = user.referral.get_children().filter(has_paid_activation = True).order_by('-activated_on')

        ########## Last Week and this week ##########
        year, week_num, day_of_week = datetime.date.today().isocalendar()
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2]-1))
        monday_of_this_week = monday_of_last_week + timedelta(days=7)
        
        sub_amount = int(self.request.user.referral.package)
        ########## Percentage Earn ##########
        if sub_amount == 20:
            first_percentage = 0.2     # 20%
            second_percentage = 0.1    # 10%
            third_percentage = 0.05    # 5%
            fourth_percentage = 0.03   # 3%
            fifth_percentage = 0.02    # 2%
            sixth_percentage = 0.01    # 1%
            seventh_percentage = 0.01  # 1%
            eigth_percentage = 0.01    # 1%
        else:
            first_percentage = 0.25    # 25%
            second_percentage = 0.125  # 12.5%
            third_percentage = 0.1     # 10%
            fourth_percentage = 0.05   # 5%
            fifth_percentage = 0.02    # 2%
            sixth_percentage = 0.01    # 1%
            seventh_percentage = 0.01  # 1%
            eigth_percentage = 0.01    # 1%
        
        first_generation_20_pack_count = first_generation.filter(package = 20).count()
        first_generation_50_pack_count = first_generation.filter(package = 50).count()
        first_generation_100_pack_count = first_generation.filter(package = 100).count()

        first_gen_20_total_earn = 20 * first_percentage * first_generation_20_pack_count
        first_gen_50_total_earn = 50 * first_percentage * first_generation_50_pack_count
        first_gen_100_total_earn = 100 * first_percentage * first_generation_100_pack_count

        first_generation_count = first_generation_20_pack_count + first_generation_50_pack_count + first_generation_100_pack_count
        first_total_earn = first_gen_20_total_earn + first_gen_50_total_earn + first_gen_100_total_earn
        
        # This Week Earn
        num_of_1st_gen_20_pack = first_generation.filter(activated_on__week=week_num).filter(package = 20).count()
        num_of_1st_gen_50_pack = first_generation.filter(activated_on__week=week_num).filter(package = 50).count()
        num_of_1st_gen_100_pack = first_generation.filter(activated_on__week=week_num).filter(package = 100).count()

        first_gen_20_week_total_earn = 20 * first_percentage * num_of_1st_gen_20_pack
        first_gen_50_week_total_earn = 50 * first_percentage * num_of_1st_gen_50_pack
        first_gen_100_week_total_earn = 100 * first_percentage * num_of_1st_gen_100_pack

        num_of_first_gen_referral_dis_week = num_of_1st_gen_20_pack + num_of_1st_gen_50_pack + num_of_1st_gen_100_pack
        first_gen_week_total_earn = first_gen_20_week_total_earn + first_gen_50_week_total_earn + first_gen_100_week_total_earn

        # Last Week Earn
        num_of_1st_gen_20_pack_last_week = first_generation.filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).filter(package = 20).count()
        num_of_1st_gen_50_pack_last_week = first_generation.filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).filter(package = 50).count()
        num_of_1st_gen_100_pack_last_week = first_generation.filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).filter(package = 100).count()

        first_gen_20_last_week_total_earn = 20 * first_percentage * num_of_1st_gen_20_pack_last_week
        first_gen_50_last_week_total_earn = 50 * first_percentage * num_of_1st_gen_50_pack_last_week
        first_gen_100_last_week_total_earn = 100 * first_percentage * num_of_1st_gen_100_pack_last_week

        num_of_first_gen_referral_last_week = num_of_1st_gen_20_pack_last_week + num_of_1st_gen_50_pack_last_week + num_of_1st_gen_100_pack_last_week
        first_gen_last_week_total_earn = first_gen_20_last_week_total_earn + first_gen_50_last_week_total_earn + first_gen_100_last_week_total_earn

        ########## Second generation ##########
        output = get_referal_logic_matrix(self, first_generation, second_percentage)

        second_total_earn = output[0] 
        second_generation = output[1]
        second_generation_count = output[2]
        second_generation_page_obj = output[3]
        second_gen_week_total_earn = output[4]
        num_of_second_gen_referral_dis_week = output[5]
        nth_gen_last_week_total_earn = output[6]

        second_gen_last_week_total_earn = nth_gen_last_week_total_earn

        ########## Third generation ########## 
        output = get_referal_logic_matrix(self, second_generation, third_percentage)

        third_total_earn = output[0] 
        third_generation = output[1]
        third_generation_count = output[2]
        third_generation_page_obj = output[3]
        third_gen_week_total_earn = output[4]
        num_of_third_gen_referral_dis_week = output[5]
        nth_gen_last_week_total_earn = output[6]

        third_gen_last_week_total_earn = nth_gen_last_week_total_earn

        ########## Fourth generation ##########
        output = get_referal_logic_matrix(self, third_generation, fourth_percentage)

        fourth_total_earn = output[0] 
        fourth_generation = output[1]
        fourth_generation_count = output[2]
        fourth_generation_page_obj = output[3]
        fourth_gen_week_total_earn = output[4]
        num_of_fourth_gen_referral_dis_week = output[5]
        nth_gen_last_week_total_earn = output[6]

        fourth_gen_last_week_total_earn = nth_gen_last_week_total_earn

        ########## Fifth generation ##########
        output = get_referal_logic_matrix(self, fourth_generation, fifth_percentage)

        fifth_total_earn = output[0] 
        fifth_generation = output[1]
        fifth_generation_count = output[2]
        fifth_generation_page_obj = output[3]
        fifth_gen_week_total_earn = output[4]
        num_of_fifth_gen_referral_dis_week = output[5]
        nth_gen_last_week_total_earn = output[6]

        fifth_gen_last_week_total_earn = nth_gen_last_week_total_earn

        ########## Sixth generation ##########
        output = get_referal_logic_matrix_3_by_3(self, fifth_generation, sixth_percentage)

        sixth_total_earn = output[0] 
        sixth_generation = output[1]
        sixth_generation_count = output[2]
        sixth_generation_page_obj = output[3]
        sixth_gen_week_total_earn = output[4]
        num_of_sixth_gen_referral_dis_week = output[5]
        nth_gen_last_week_total_earn = output[6]

        sixth_gen_last_week_total_earn = nth_gen_last_week_total_earn

        ########## Seventh generation ##########
        output = get_referal_logic_matrix_3_by_3(self, sixth_generation, seventh_percentage)

        seventh_total_earn = output[0] 
        seventh_generation = output[1]
        seventh_generation_count = output[2]
        seventh_generation_page_obj = output[3]
        seventh_gen_week_total_earn = output[4]
        num_of_seventh_gen_referral_dis_week = output[5]
        nth_gen_last_week_total_earn = output[6]

        seventh_gen_last_week_total_earn = nth_gen_last_week_total_earn

        ########## Eigth generation ##########
        output = get_referal_logic_matrix_3_by_3(self, seventh_generation, eigth_percentage)

        eigth_total_earn = output[0] 
        eigth_generation = output[1]
        eigth_generation_count = output[2]
        eigth_generation_page_obj = output[3]
        eigth_gen_week_total_earn = output[4]
        num_of_eigth_gen_referral_dis_week = output[5]
        nth_gen_last_week_total_earn = output[6]

        eigth_gen_last_week_total_earn = nth_gen_last_week_total_earn

        ##### Condition for Adding 6th, 7th and 8th generation to weekly refer earn #####
        if sixth_generation_count != 0 and sixth_generation_count%30 == 0:
            sixth_gen_week_total_earn_con = sixth_gen_week_total_earn
            sixth_gen_last_week_total_earn_con = sixth_gen_last_week_total_earn    
        elif sixth_generation_count%30 != 0 and not sixth_generation_count < 30:
            sixth_gen_week_total_earn_con = sixth_gen_week_total_earn
            sixth_gen_last_week_total_earn_con = sixth_gen_last_week_total_earn   
        else:
            sixth_gen_week_total_earn_con = 0.00
            sixth_gen_last_week_total_earn_con = 0.00
            
        if seventh_generation_count != 0 and seventh_generation_count%30 == 0:
            seventh_gen_week_total_earn_con = seventh_gen_week_total_earn
            seventh_gen_last_week_total_earn_con = seventh_gen_last_week_total_earn
        elif seventh_generation_count%30 != 0 and not seventh_generation_count < 30:
            seventh_gen_week_total_earn_con = seventh_gen_week_total_earn
            seventh_gen_last_week_total_earn_con = seventh_gen_last_week_total_earn    
        else:
            seventh_gen_week_total_earn_con = 0.00
            seventh_gen_last_week_total_earn_con = 0.00
            
        if eigth_generation_count != 0 and eigth_generation_count%30 == 0:
            eigth_gen_week_total_earn_con = eigth_gen_week_total_earn
            eigth_gen_last_week_total_earn_con = eigth_gen_last_week_total_earn
        elif eigth_generation_count%30 != 0 and not eigth_generation_count < 30:
            eigth_gen_week_total_earn_con = eigth_gen_week_total_earn
            eigth_gen_last_week_total_earn_con = eigth_gen_last_week_total_earn
        else:
            eigth_gen_week_total_earn_con = 0.00
            eigth_gen_last_week_total_earn_con = 0.00
        
        # Total Earn    
        total_earn = first_total_earn + second_total_earn + third_total_earn + fourth_total_earn + fifth_total_earn + sixth_total_earn + seventh_total_earn + eigth_total_earn
            
        # This Week
        total_weekly_earn = first_gen_week_total_earn + second_gen_week_total_earn + third_gen_week_total_earn + fourth_gen_week_total_earn + fifth_gen_week_total_earn + sixth_gen_week_total_earn_con + seventh_gen_week_total_earn_con + eigth_gen_week_total_earn_con
        
        # Last Weeek
        total_last_weekly_earn = first_gen_last_week_total_earn + second_gen_last_week_total_earn + third_gen_last_week_total_earn + fourth_gen_last_week_total_earn + fifth_gen_last_week_total_earn + sixth_gen_last_week_total_earn_con + seventh_gen_last_week_total_earn_con + eigth_gen_last_week_total_earn_con

        user_wallet = Wallet.objects.get(user = self.request.user)
        
        user_wallet_balance_before = user_wallet.current_balance
        weekly_earn_bonus_before = user_wallet.weekly_earn_bonus
        
        # Condition to add Earn Amount to Wallet Balance
        if not int(total_weekly_earn) == 0:
            difference_in_weekly_earn = float(total_weekly_earn) - float(weekly_earn_bonus_before)
            amount_to_add = float(weekly_earn_bonus_before) + float(difference_in_weekly_earn)
            user_wallet.weekly_earn_bonus = amount_to_add
        elif int(total_weekly_earn) == 0:
            difference_in_weekly_earn = float(total_weekly_earn) - float(weekly_earn_bonus_before) + float(weekly_earn_bonus_before)
            amount_to_add = float(weekly_earn_bonus_before) + float(difference_in_weekly_earn) - float(weekly_earn_bonus_before)
            user_wallet.weekly_earn_bonus = amount_to_add
        
        new_wallet_balance =  float(user_wallet_balance_before) + float(difference_in_weekly_earn)
        user_wallet.current_balance = new_wallet_balance
        user_wallet.weekly_retained_earn_bonus = total_last_weekly_earn 
        user_wallet.save()
        
        amount_earn_so_far = float(total_earn)
        user_wallet.weekly_earn_bonus_so_far = amount_earn_so_far
        user_wallet.save()
        
        ########## Return Resposes ##########
        if query_view == 1:
            response = first_generation
        elif query_view == 2:
            response = second_generation
        elif query_view == 3:
            response = third_generation
        elif query_view == 4:
            response = fourth_generation
        elif query_view == 5:
            response = fifth_generation
        elif query_view == 6:
            response = sixth_generation
        elif query_view == 7:
            response = seventh_generation
        elif query_view == 8:
            response = eigth_generation

        for i in second_generation:
            print('This is sponsor: ', i.get_parent())

        return response

#################   REFERAL LOGIC MATRIX   #################
def get_referal_logic_matrix(self, previous_generation, nth_percentage):
    ########## Last Week and this week ##########
    year, week_num, day_of_week = datetime.date.today().isocalendar()
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2]-1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)

    ########## 2nd => 5th generation ##########
    nth_gen = []
    nth_generation_count = None
    nth_generation_20_pack_count = 0
    nth_generation_50_pack_count = 0
    nth_generation_100_pack_count = 0
    num_of_nth_gen_20_pack_dis_week = 0
    num_of_nth_gen_50_pack_dis_week = 0
    num_of_nth_gen_100_pack_dis_week = 0
    num_of_nth_gen_20_pack_last_week = 0
    num_of_nth_gen_50_pack_last_week = 0
    num_of_nth_gen_100_pack_last_week = 0
    for i in previous_generation:
        nth_gen += i.get_children().filter(has_paid_activation = True)
        
        nth_generation_20_pack_count += i.get_children().filter(has_paid_activation = True).filter(package = 20).count()
        nth_generation_50_pack_count += i.get_children().filter(has_paid_activation = True).filter(package = 50).count()
        nth_generation_100_pack_count += i.get_children().filter(has_paid_activation = True).filter(package = 100).count()
        
        # This week
        num_of_nth_gen_20_pack_dis_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__week=week_num).filter(package = 20).count()
        num_of_nth_gen_50_pack_dis_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__week=week_num).filter(package = 50).count()
        num_of_nth_gen_100_pack_dis_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__week=week_num).filter(package = 100).count()
        
        # Last Week
        num_of_nth_gen_20_pack_last_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).filter(package = 20).count()
        num_of_nth_gen_50_pack_last_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).filter(package = 50).count()
        num_of_nth_gen_100_pack_last_week += i.get_children().filter(has_paid_activation = True).filter(package = 100).filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).count()
        
    nth_generation = nth_gen

    # Total nth Generation Earn
    nth_gen_20_total_earn = 20 * nth_percentage * nth_generation_20_pack_count
    nth_gen_50_total_earn = 50 * nth_percentage * nth_generation_50_pack_count
    nth_gen_100_total_earn = 100 * nth_percentage * nth_generation_100_pack_count

    nth_total_earn = nth_gen_20_total_earn + nth_gen_50_total_earn + nth_gen_100_total_earn
    
    nth_generation_count = nth_generation_20_pack_count + nth_generation_50_pack_count + nth_generation_100_pack_count

    # This week
    num_of_nth_gen_referral_dis_week = num_of_nth_gen_20_pack_dis_week + num_of_nth_gen_50_pack_dis_week + num_of_nth_gen_100_pack_dis_week

    nth_gen_20_pack_week_total_earn = 20 * nth_percentage * num_of_nth_gen_20_pack_dis_week
    nth_gen_50_pack_week_total_earn = 50 * nth_percentage * num_of_nth_gen_50_pack_dis_week
    nth_gen_100_pack_week_total_earn = 100 * nth_percentage * num_of_nth_gen_100_pack_dis_week

    nth_gen_week_total_earn = nth_gen_20_pack_week_total_earn + nth_gen_50_pack_week_total_earn + nth_gen_100_pack_week_total_earn
    
    # Last Week
    num_of_nth_gen_referral_last_week = num_of_nth_gen_20_pack_last_week + num_of_nth_gen_50_pack_last_week + num_of_nth_gen_100_pack_last_week

    nth_gen_20_pack_last_week_total_earn = 20 * nth_percentage * num_of_nth_gen_20_pack_last_week
    nth_gen_50_pack_last_week_total_earn = 50 * nth_percentage * num_of_nth_gen_50_pack_last_week
    nth_gen_100_pack_last_week_total_earn = 100 * nth_percentage * num_of_nth_gen_100_pack_last_week

    nth_gen_last_week_total_earn = nth_gen_20_pack_last_week_total_earn + nth_gen_50_pack_last_week_total_earn + nth_gen_100_pack_last_week_total_earn

    output = [nth_total_earn, nth_generation, nth_generation_count, nth_generation, nth_gen_week_total_earn, num_of_nth_gen_referral_dis_week, nth_gen_last_week_total_earn]

    return output

#################   REFERAL LOGIC MATRIX 3x3   #################
def get_referal_logic_matrix_3_by_3(self, previous_generation, nth_percentage):

    ########## Last Week and this week ##########
    year, week_num, day_of_week = datetime.date.today().isocalendar()
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2]-1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)

    ########## 6th => 8th generation ##########
    nth_gen = []
    nth_generation_count = None
    nth_generation_20_pack_count = 0
    nth_generation_50_pack_count = 0
    nth_generation_100_pack_count = 0
    num_of_nth_gen_20_pack_dis_week = 0
    num_of_nth_gen_50_pack_dis_week = 0
    num_of_nth_gen_100_pack_dis_week = 0
    num_of_nth_gen_20_pack_last_week = 0
    num_of_nth_gen_50_pack_last_week = 0
    num_of_nth_gen_100_pack_last_week = 0

    for i in previous_generation:
        nth_gen += i.get_children().filter(has_paid_activation = True).order_by('-activated_on')

        nth_generation_20_pack_count += i.get_children().filter(has_paid_activation = True).filter(package = 20).count()
        nth_generation_50_pack_count += i.get_children().filter(has_paid_activation = True).filter(package = 50).count()
        nth_generation_100_pack_count += i.get_children().filter(has_paid_activation = True).filter(package = 100).count()

        # This week
        num_of_nth_gen_20_pack_dis_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__week=week_num).filter(package = 20).count()
        num_of_nth_gen_50_pack_dis_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__week=week_num).filter(package = 50).count()
        num_of_nth_gen_100_pack_dis_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__week=week_num).filter(package = 100).count()
        
        # Last Week
        num_of_nth_gen_20_pack_last_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).filter(package = 20).count()
        num_of_nth_gen_50_pack_last_week += i.get_children().filter(has_paid_activation = True).filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).filter(package = 50).count()
        num_of_nth_gen_100_pack_last_week += i.get_children().filter(has_paid_activation = True).filter(package = 100).filter(activated_on__gte=monday_of_last_week, activated_on__lt=monday_of_this_week).count()
        
    nth_generation = nth_gen
    nth_generation_count = nth_generation_20_pack_count + nth_generation_50_pack_count + nth_generation_100_pack_count
    thirty_user_is_equal_to_one_user = 30

    # Total nth Generation Earn
    if nth_generation_count != 0 and nth_generation_count%30 == 0:
        nth_gen_20_total_earn = 20 * nth_percentage * thirty_user_is_equal_to_one_user
        nth_gen_50_total_earn = 50 * nth_percentage * thirty_user_is_equal_to_one_user
        nth_gen_100_total_earn = 100 * nth_percentage * thirty_user_is_equal_to_one_user
        nth_total_earn = nth_gen_20_total_earn + nth_gen_50_total_earn + nth_gen_100_total_earn
    elif nth_generation_count%30 != 0 and not nth_generation_count < 30: 
        nth_gen_20_total_earn = 20 * nth_percentage * thirty_user_is_equal_to_one_user
        nth_gen_50_total_earn = 50 * nth_percentage * thirty_user_is_equal_to_one_user
        nth_gen_100_total_earn = 100 * nth_percentage * thirty_user_is_equal_to_one_user
        nth_total_earn = nth_gen_20_total_earn + nth_gen_50_total_earn + nth_gen_100_total_earn
    else:
        nth_total_earn = 0
        
    # This Week
    num_of_nth_gen_referral_dis_week = num_of_nth_gen_20_pack_dis_week + num_of_nth_gen_50_pack_dis_week + num_of_nth_gen_100_pack_dis_week

    nth_gen_20_pack_week_total_earn = 20 * nth_percentage * num_of_nth_gen_20_pack_dis_week
    nth_gen_50_pack_week_total_earn = 50 * nth_percentage * num_of_nth_gen_50_pack_dis_week
    nth_gen_100_pack_week_total_earn = 100 * nth_percentage * num_of_nth_gen_100_pack_dis_week

    nth_gen_week_total_earn = nth_gen_20_pack_week_total_earn + nth_gen_50_pack_week_total_earn + nth_gen_100_pack_week_total_earn
    
    # Last Week
    num_of_nth_gen_referral_last_week = num_of_nth_gen_20_pack_last_week + num_of_nth_gen_50_pack_last_week + num_of_nth_gen_100_pack_last_week

    nth_gen_20_pack_last_week_total_earn = 20 * nth_percentage * num_of_nth_gen_20_pack_last_week
    nth_gen_50_pack_last_week_total_earn = 50 * nth_percentage * num_of_nth_gen_50_pack_last_week
    nth_gen_100_pack_last_week_total_earn = 100 * nth_percentage * num_of_nth_gen_100_pack_last_week

    nth_gen_last_week_total_earn = nth_gen_20_pack_last_week_total_earn + nth_gen_50_pack_last_week_total_earn + nth_gen_100_pack_last_week_total_earn
    
    output = [nth_total_earn, nth_generation, nth_generation_count, nth_generation, nth_gen_week_total_earn, num_of_nth_gen_referral_dis_week, nth_gen_last_week_total_earn]

    return output