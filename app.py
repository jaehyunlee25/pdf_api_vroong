from flask import Flask, render_template, send_file
from flask import request
from flask_cors import CORS, cross_origin
import json
from fpdf import FPDF

app = Flask(__name__)
CORS(app)

@app.route('/hello')
def hello():
    return 'hello, world!!'
@app.route('/pdf/order', methods=['POST'])
def order():    
    param = json.loads(request.get_data(), encoding='utf-8')
    if (param['type'] == 'dawn'): dawn(param)
    elif (param['type'] == 'fulfillment'): fulfillment(param)
    return send_file('pdf/' + param['orderNumber'] + '.pdf')

@app.route('/pdf/<order_number>')
def download(order_number):
    return send_file('pdf/' + order_number + '.pdf')

def fulfillment(param):
    pdf = FPDF()
    pdf.add_page()
    pdf.image('img/fulfillment_1page.jpg', 0, 0, 210, 295)
    pdf.add_font('NanumGothicCoding', '', '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf', uni=True)
    pdf.set_font("NanumGothicCoding", size = 7)
    pdf.set_stretching(85.0)

    pdf.text(8.3, 39.2, param['orderNumber'])    # 문서번호 위치
    pdf.text(14.7, 43, param['company'])    # 수신
    pdf.text(14.7, 51.4, param['date_kor'])    # 날짜
    pdf.text(14.7, 55.7, '풀필먼트 서비스 용역 예상 견적서')    # 제목

    xs = {'극소형': 53, '소형': 85, '중형': 117, '대형': 149, '비고': 181}
    ys = {'세변합': 102.3, '중량': 108.5}
    pdf.text(xs[param['size']], ys['세변합'], param['sum'])    # 견적금액 세변합
    pdf.text(xs[param['size']], ys['중량'], param['weight'])    # 견적금액 중량

    ys = {'입고료': 124.5, '하차비': 131.5, '출고비(상온)': 138.5}
    pdf.text(xs[param['size']], ys['입고료'], param['in'])    # 유통가공비 입고료
    pdf.text(xs[param['size']], ys['하차비'], param['down'])    # 유통가공비 하차비
    pdf.text(xs[param['size']], ys['출고비(상온)'], param['out'])    # 유통가공비 출고비(상온)

    ys = {'일반상품': 161.5, '식품(아이스박스)': 168.1}
    pdf.text(xs[param['size']], ys['일반상품'], param['normal'])    # 택배비 일반상품
    pdf.text(xs[param['size']], ys['식품(아이스박스)'], param['food'])    # 택배비 식품(아이스박스)

    xs = {'상온': 94, '냉장/냉동': 142, '비고': 183}
    pdf.text(xs[param['temperature']], 187.3, param['storage'])    # 택배비 보관료

    pdf.set_font("NanumGothicCoding", size = 12)
    pdf.set_stretching(72.5)
    pdf.text(94, 264.3, param['date'])    # 견적 일자

    pdf.add_page()
    pdf.image('img/fulfillment_2page.jpg', 0, 0, 210, 295)

    fileName = param['orderNumber']+'.pdf'

    pdf.output('pdf/' + fileName)

def dawn(param):
    pdf = FPDF()
    pdf.add_page()
    pdf.image('img/dawn_1page.jpg', 0, 0, 210, 295)
    pdf.add_font('NanumGothicCoding', '', '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf', uni=True)
    pdf.set_font("NanumGothicCoding", size = 7)
    pdf.set_stretching(85.0)

    pdf.text(8.3, 39.2 + 4.2, param['orderNumber'])    # 문서번호 위치
    pdf.text(14.7, 43 + 4.2, param['company'])    # 수신
    pdf.text(14.7, 51.4 + 4.2, param['date_kor'])    # 날짜
    pdf.text(14.7, 55.7 + 4.2, '새벽배송 예상 견적서')    # 제목

    # 배송료
    xs = {'물동량': 60, '소형': 98, '중형': 135.9, '대형': 176}
    pdf.text(xs['물동량'], 109, param['flow'])    # 
    pdf.text(xs[param['size']], 109, param['price'])    # 배송료

    # 박스추가
    xs = {'plus': 112, '대형': 172}
    ys = {'세변합': 129.3, '중량': 136.5}
    pdf.text(xs[param['option']], ys['세변합'], param['sum'])    # 세변합
    pdf.text(xs[param['option']], ys['중량'], param['weight'])    # Box당 최대 중량

    pdf.set_font("NanumGothicCoding", size = 12)
    pdf.set_stretching(72.5)
    pdf.text(94, 264.3, param['date'])    # 견적 일자

    fileName = param['orderNumber']+'.pdf'

    pdf.output('pdf/' + fileName)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)