import pickle

#관리자모드 - 상품추가
'''기존 사용자와 첫 사용자-상품등록메뉴 : 이름, 상품단가, 거래단가 등 세팅->
종료(저장)-> start_menu(기존 사용자와 동일)'''

NUM_OF_MENU = 8

#goods = [ '', '아메리카노', '연유라떼', '딸기스무디', '핫초코', '과일빙수']
goods = [""]*NUM_OF_MENU                       #상품명
#price = [ 0, 3500, 4000, 4500, 3500, 8000 ]
price = [0]*NUM_OF_MENU                             #상품가격
#trade_price = [ 0, 900, 1500, 2000, 1100, 3800 ]
trade_price = [0]*NUM_OF_MENU               #거래단가
#stock = [0, 20, 15, 15, 20, 10 ]
stock = [0]*NUM_OF_MENU                           #상품재고
order_stock = [0]*NUM_OF_MENU                   #총입고수량
total_amount = [0]*NUM_OF_MENU                  #누적판매수량
amount = [0]*NUM_OF_MENU                        #구매갯수
total = [0]*NUM_OF_MENU                             #각 상품별 금액 합계
pay = 0
#password = "0000"
password = ""

#----------------------------
def start_system():
    while True:
        print('======== 사용자 설정 ========')
        print('1. 기존 사용자\n2. 신규 사용자')
        user = int(input('사용자를 선택하여 주십시오.'))
        if user == 1:
            start_menu()
            break
        elif user == 2:
            setting_menu()
            end_menu()
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요')
    
#----------------------------
def setting_menu():
    global goods, price, stock, password, trade_price
    new_name = ""
    new_price = 0
    new_stock = 0
    new_password = '0000'
    new_tPrice = 0
    flag = '1'
    pFlag = '0'
    count = 1
    
    print('======== 메뉴 세팅 = ========')
    #goods, price, stock, password, trade_price
    flag = input('상품을 등록하시겠습니까?(예: 1/Y, 아니오: 0/N)')
    while flag in [ 'Y', 'y', '1' ]:
        new_name = input('상품명을 입력해주세요.')
        if new_name in goods:
            print('이미 존재하는 상품명입니다. 다시 입력해주세요')
            continue
        if new_name == "":
            print('다시 입력해주세요')
            continue
        goods[count] = new_name

        print(new_name, '의 판매단가를 입력해주세요.')
        new_price = int(input())
        if new_price < 0:
            print('가격은 0원 이하일 수 없습니다. 다시 입력해주세요')
            continue
        price[count] = new_price

        print(new_name, '의 거래단가를 입력해주세요.')
        new_tPrice = int(input())
        if new_tPrice < 0:
            print('가격은 0원 이하일 수 없습니다. 다시 입력해주세요')
            continue
        trade_price[count] = new_tPrice

        print(new_name, '의 초기재고를 입력해주세요.')
        new_stock = int(input())
        if new_stock < 0:
            print('재고는 0개 이하일 수 없습니다. 다시 입력해주세요.')
            continue
        stock[count] = new_stock

        flag = input('상품을 더 추가하시겠습니까?(예: 1/Y, 아니오: 0/N)')

        count += 1
        
    flag = input('비밀번호를 설정하시겠습니까? (입력하지 않으면 0000으로 설정됩니다. 예: 1/Y, 아니오: 0/N)')
    while flag in [ 'Y', 'y', '1' ]:
        new_password = input('설정할 비밀번호를 입력해주세요.')
        if new_password == '0000':
            print('새로운 비밀번호를 입력해주세요.')
        password = new_password
        break

#------------------------------
    
def start_menu():
    num = 0

    read_data()
    while num != 3:
        print('======== 메인 메뉴 ========')
        print('1. 상품판매\n2. 재고관리\n3. 종료\n4. 관리자모드')
        print('=======================')
        num = int(input('어떤 업무를 하시겠습니까?'))
        if num == 1:
            run_sale()
        elif num == 2:
            run_control()
        elif num == 3:
            end_menu()
        elif num == 4:
            if check_password():
                run_manager()
        else:
            print('다시 선택해주십시오.')


#------------------------------------------
           
def show_menu():
    print('========= 상품 메뉴 ========')
    for i in range(1, len(goods)):
        print(i, '. ', goods[i], '\t', price[i], '원 ', stock[i], '개')
    print('========================')

#------------------------------------------
def select_menu():
    global amount, stock, total
    goods_num = 0
    num = 0
    flag = 'y'
    while flag in [ 'Y', 'y' ,'1' ]:
        goods_num = int(input('어떤 상품을 구매하시겠습니까?')) #엔터쳤을 때 오류
        if goods_num < 1 or goods_num > len(goods):
            print('잘못 입력하셨습니다. 다시 선택해주세요.')
            break
        print(goods[goods_num], '을 선택하셨습니다.')
        print('단가는', price[goods_num], '원입니다.')

        num = int(input('몇 개를 구매하시겠습니까?'))
        if num < 0:
            print('잘못된 입력입니다. 다시 입력해주세요')
            continue
        if num > stock[goods_num]:
            print('재고가 부족합니다. 남은 재고는', stock[goods_num], '개 입니다')
            continue

        amount[goods_num] += num
        total_amount[goods_num] += num
        stock[goods_num] -= num
        total[goods_num] += num*price[goods_num]
        flag = input('더 구매하시겠습니까?(예: 1/Y, 아니오: 0/N)')
#----------------------------------------
def delete_menu():
    global amount, stock, total
    goods_num = 0
    num = 0
    flag = '0'

    print('===========================')
    print('품목               수량       금액    ')
    for i in range(1, len(goods)):
        if amount[i] > 0:
            print('%s %8.f %8.0f' %(goods[i], amount[i], total[i]) + '원')
    print('총구매금액                  ', sum(total), '원')
    
    flag = input('상품을 취소하시겠습니까?(예: 1/Y, 아니오: 0/N)')
    while flag in ['Y', 'y', '1' ]:
        goods_num = int(input('어떤 상품을 취소하시겠습니까?'))
        if goods_num < 1 or goods_num > len(goods) or amount[goods_num] < 1:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue

        print(goods[goods_num],' 몇 개를 취소하시겠습니까?')
        num = int(input())
        if num < 0 or num > amount[goods_num]:
            print('잘못 입력하셨습니다. 다시 입력해주세요')
            continue

        amount[goods_num] -= num
        stock[goods_num] += num
        total[goods_num] -= price[goods_num]*num
        
        flag = input('상품을 더 취소하시겠습니까?(예: 1/Y, 아니오: 0/N)')
        
#----------------------------------------
def show_pay():
    global pay
    print('구매하신 총 금액은', sum(total), '입니다')
    while pay < sum(total):
        print('결제금액을 입금해주시기 바랍니다.')
        pay += int(input('결제 금액: '))
        if pay < sum(total):
            print('결제금액에서', sum(total)-pay, '원이 부족합니다.')

#----------------------------------------
            
def show_rec():
    print('======== 영 수 증 ========')
    print('품목               수량       금액    ')
    for i in range(1, len(goods)):
        if amount[i] > 0:
            print('%s %8.f %8.0f' %(goods[i], amount[i], total[i]) + '원')

    print('총구매금액                  ', sum(total), '원')
    print('받은금액                     ', pay, '원')
    print('거스름돈                     ', pay-sum(total), '원')
    print('감사합니다~ 좋은 하루 되세요!')
#----------------------------------------

def run_sale():
    global amount, total, pay
    for i in range(1, len(goods)): #amount.clear() -> 새로 만들기?
        amount[i] = 0
        total[i] = 0
        pay = 0
    print(amount)
    print(total)
    print(total_amount)
    show_menu()
    select_menu()
    delete_menu()
    show_pay()
    show_rec()
    
#----------------------------------------

def run_control():
    num = 0
    while num != 4:
        print('======== 재고관리 ========')
        print('1. 재고조회\n2. 상품입고\n3. 상품반품\n4. 이전메뉴')
        num = int(input('어떤 업무를 하시겠습니까?'))
        if num == 1:
            check_stock()
        elif num == 2:
            get_stock()
        elif num == 3:
            return_stock()
        elif num == 4:
            return
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')

#----------------------------------------
        
def check_stock():
    print('======== 재고조회 ========')
    print('품목               금액         재고')
    for i in range(1, len(goods)):
        print(i, '.', goods[i], '      ', price[i], '    ', stock[i])
    
#-----------------------------------------
        
def get_stock():
    while True:
        goods_num = int(input('어떤 상품을 입고하시겠습니까?'))
        if goods_num < 1 or goods_num > len(goods) -1:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue
        
        print(goods[goods_num], ' 몇 개를 입고하시겠습니까?')
        num = int(input())
        if num < 0:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue

        stock[goods_num] += num
        order_stock[goods_num] += num
        print(goods[goods_num], num, '개를 입고하였습니다.')
        break
        
#----------------------------------------
    
def return_stock():
    while True:
        goods_num = int(input('어떤 상품을 반품하시겠습니까?'))
        if goods_num < 1 or goods_num > len(goods) - 1:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue
        
        print(goods[goods_num], ' 몇 개를 반품하시겠습니까?')
        num = int(input())
        if num > stock[goods_num] or num < 0:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue

        stock[goods_num] -= num
        print(goods[goods_num], num, '개를 반품하였습니다.')
        break

#-----------------------------------------

def end_menu(): #함수화하기
    try:
        outfile = open('goods.txt', 'wb')
        pickle.dump(goods, outfile)
    finally:
        outfile.close()

    try:
        outfile = open('price.txt', 'wb')
        pickle.dump(price, outfile)
    finally:
        outfile.close()

    try:
        outfile = open('stock.txt', 'wb')
        pickle.dump(stock, outfile)
    finally:
        outfile.close()

    try:
        outfile = open('password.txt', 'wb')
        pickle.dump(password, outfile)
    finally:
        outfile.close()

    try:
        outfile = open('trade_price.txt', 'wb')
        pickle.dump(trade_price, outfile)
    finally:
        outfile.close()

    print('프로그램을 종료합니다.')

#-----------------------------------------

def read_data():
    global goods, price, stock, password, trade_price
    try:
        infile = open('goods.txt', 'rb')
        goods = pickle.load(infile)
        print(goods)
    finally:
        infile.close()

    try:
        infile = open('price.txt', 'rb')
        price = pickle.load(infile)
        print(price)
    finally:
        infile.close()

    try:
        infile = open('stock.txt', 'rb')
        stock = pickle.load(infile)
        print(stock)
    finally:
        infile.close()

    try:
        infile = open('password.txt', 'rb')
        password = pickle.load(infile)
        print(password)
    finally:
        infile.close()

    try:
        infile = open('trade_price.txt', 'rb')
        trade_price = pickle.load(infile)
        print(trade_price)
    finally:
        infile.close()
#------------------------------------------

def check_password():
    while True:
        tmp = input('비밀번호 확인 :  (종료 : 0)')
        if tmp == '0':
            return
        if tmp != password:
            print('비밀번호가 다릅니다. 다시 입력해주세요')
            continue
        return True


#-------------------------------------------
    
#관리자모드
        
def run_manager():
    num = 0

    while num != 5:
        print('======== 관리자 모드 ========')
        print('1. 상품조회\n2. 상품변경\n3. 단가변경\n4. 매출실적현황\n5. 이전메뉴\n6. 비밀번호설정')
        num = int(input('어떤 업무를 하시겠습니까?'))

        if num == 1:
            check_goods()
        elif num == 2:
            change_goods()
        elif num == 3:
            change_price()
        elif num == 4:
            sales_status()
        elif num == 5:
            return
        elif num == 6:
            change_password()
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요')
        
#-----------------------------------------
        
def check_goods():
    print('======== 상품 조회 ========')
    print('상품명\t\t단가')
    for i in range(1, len(goods)):
        print(i, '.', goods[i], '\t', price[i])

#----------------------------------------
        
def change_goods():
    global goods
    new_name = ""
    goods_num = 0
    print('======== 상품 변경 ========')
    while True:
        goods_num = int(input('어떤 상품의 이름을 변경하시겠습니까?(숫자로 입력)')) #상품명으로 입력되게
        if goods_num < 1 or goods_num > NUM_OF_MENU - 1:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue
        print(goods[goods_num], '을 어떤 이름으로 변경하시겠습니까?')
        new_name = input()
        if new_name in goods:
            print('이미 존재하는 상품명입니다. 다시 입력해주세요')
            continue

        print(goods[goods_num], '의 상품명을', new_name, ' 으로 변경하였습니다.')
        goods[goods_num] = new_name
        break
    
#----------------------------------------
        
def change_price():
    global price
    new_price = 0
    goods_num = 0
    print('======== 단가 변경 ========')
    while True:
        goods_num = int(input('어떤 상품의 단가를 변경하시겠습니까?'))
        if goods_num < 1 or goods_num > NUM_OF_MENU - 1:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue

        print(goods[goods_num], '의 단가는', price[goods_num], '입니다. 얼마로 변경하시겠습니까?')
        new_price = int(input())
        if new_price < 0:
            print('가격을 0원보다 낮게 설정할 수 없습니다. 다시 입력해주세요')
            continue

        print(goods[goods_num], '의 가격을', price[goods_num], '원에서', new_price, '원으로 변경하였습니다.')
        price[goods_num] = new_price
        break
    
#---------------------------------------
        
def sales_status():
    num = 0
    while num != 4:
        print('======== 매출실적현황 ========')
        print('1. 매출현황조회\n2. 주문상품조회\n3. 거래처현황\n4.이전메뉴')
        print('==========================')
        num = int(input('어떤 업무를 하시겠습니까?'))
        if num < 1 or num > 4:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue

        if num == 1:
            check_sales()
        elif num == 2:
            check_order()
        elif num == 3:
            customer_status()
        elif num == 4:
            return
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')

#-------------------------------------------
        
def change_password():
    global password
    tmp = ""
    new_password = ""
    while tmp != '0':
        print('======== 비밀번호변경 ========')
        tmp = input('비밀번호 확인 :  (종료 : 0)')
        if tmp == '0':
            return
        if tmp != password:
            print('비밀번호가 다릅니다. 다시 입력해주세요')
            continue

        new_password = input('새로운 비밀번호를 입력해주세요.')
        if new_password == password:
            print('같은 비밀번호로 변경할 수 없습니다. 다시 입력해주세요')
            continue

        password = new_password
        print('비밀번호가 변경되었습니다.')
        break
    
#-------------------------------------------
#관리자모드 - 매출실적현황


def check_sales():
    sum = 0
    print('======== 매출현황조회 ========')
    print('상품명\t\t누적판매수량\t\t누적판매금액')
    for i in range(1, len(goods)):
        tmp = total_amount[i]*price[i]
        print(goods[i], '\t\t\t', total_amount[i], '\t\t', tmp)
        sum += tmp
    print('\t\t\t전체매출금액\t', sum)

#-------------------------------------------
    
def check_order():
    flag = 0
    print('======== 주문상품조회 ========')
    print('상품명\t\t현재재고수량')
    for i in range(1, len(goods)):
        if stock[i] < 3:
            print(goods[i], '\t', stock[i])
            flag = 1

    if flag == 0:
        print('주문할 상품이 없습니다.')
        
#--------------------------------------------
        
def customer_status():
    num = 0
    while num != 4:
        print('======== 거래처현황 ========')
        print('1. 거래품목 현황조회\n2. 거래품목 입고 현황조회\n3. 거래단가 변경\n4.이전메뉴')
        num = int(input('어떤 업무를 하시겠습니까?'))

        if num == 1:
            check_tradeItem()
        elif num == 2:
            check_warehouse()
        elif num == 3:
            change_tradePrice()
        elif num == 4:
            return
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요')


#-------------------------------------------
#관리자모드 - 매출실적현황 - 거래처현황
def check_tradeItem():
    print('======== 거래품목 현황조회 ========')
    print('상품명\t\t판매단가\t거래단가')
    for i in range(1, len(goods)):
        print(goods[i], '\t\t', price[i], '\t', trade_price[i])
    
#-------------------------------------------
        
def check_warehouse():
    total_price = [0]*NUM_OF_MENU
    print('======== 거래품목 입고 현황조회 ========')
    print('상품명\t\t총입고수량\t제품별결제')
    for i in range(1, len(goods)):
        if order_stock[i] > 0:
            total_price[i] = order_stock[i] * trade_price[i]
            print(goods[i], '\t\t', order_stock[i], '\t', total_price[i])
    print('\t\t\t\t전체 결제금액 : ', sum(total_price))
    
#-------------------------------------------
def change_tradePrice():
    new_price = 0
    flag = '0'
    while True:
        print('======== 거래단가 변경 ========')
        
        goods_num = int(input('어떤 메뉴의 거래단가를 변경하시겠습니까?'))
        if goods_num > NUM_OF_MENU - 1 or goods_num < 0:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue
        
        print(goods[goods_num], '의 거래단가를 얼마로 변경하시겠습니까?')
        new_tPrice = int(input())
        if new_tPrice < 0:
            print('가격은 0원 이하일 수 없습니다. 다시 입력해주세요')
            continue
        print(goods[goods_num],' 의 거래단가를', trade_price[goods_num],
              '원에서', new_tPrice, '원으로 변경하였습니다.')
        trade_price[goods_num] = new_tPrice
        
        flag = input('판매단가를 변경하시겠습니까? (예: 1/Y, 아니오: 0/N)')
        if flag in ['Y', 'y', '1']:
            while new_price >= 0:
                print(goods[goods_num], '의 판매단가를 얼마로 변경하시겠습니까?')
                new_price = int(input())
                if new_price > 0:
                    break
                print('가격은 0원 이하일 수 없습니다. 다시 입력해주세요.')

            print(goods[goods_num], '의 판매단가를', price[goods_num], '원에서',
                  new_price, '원으로 변경하였습니다.')
            price[goods_num] = new_price
        break

#-----------------------------------
    
start_system()

        
