import streamlit as st
import time


def stream_text(text, delay=0.005):
    """텍스트를 스트리밍 방식으로 출력"""
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(full_text)
        time.sleep(delay)
    return placeholder


def calculate_price(
    current_price, step_idx, base_min=2700, base_max=3000, beta=0.5, N=7
):
    """
    3~9단계(= step_idx=3..9)에 공식 적용:
      i = step_idx - 2
      ΔP = (base_max - base_min)/N
      r_i = beta + (i-1)/(N-1)
      P_new = current_price + round(ΔP * r_i)
    """
    i = step_idx - 2
    if i < 1 or i > N:
        return current_price
    delta_p = (base_max - base_min) / N
    r_i = beta + (i - 1) / (N - 1)
    return int(round(current_price + delta_p * r_i, -1))


BRAND_INFO = [
    """AquaDew는 2023년 연 매출 3억 원을 기록하며 전년 대비 150% 성장하였습니다. 이는 우리의 대표 제품인 '딥 모이스처 크림'이 출시 이후 15,000개 이상 판매된 결과입니다. 
    이러한 성과는 20~40대 여성 소비층을 중심으로 한 강력한 시장 반응을 반영하며, 이는 귀사와의 협력을 통해 더욱 확대될 것입니다. 우리의 성장세는 귀사의 생산량 증가로 이어질 것이며, 이는 귀사의 수익성 향상에 기여할 것입니다. 
제조사에서 초기 단가를 맞춰주시면, 지속적인 발주 증가와 함께 장기적인 협력을 이어갈 수 있습니다.""",
    """AquaDew는 소셜미디어를 활용한 홍보 전략을 구축하고 있으며, 특히 수분 케어 관련 뷰티 인플루언서와의 협업을 통해 콘텐츠 마케팅을 강화할 예정입니다. 
    이러한 마케팅 계획은 제품의 인지도를 높이고 판매량을 증가시킬 것입니다. 귀사는 이러한 마케팅 활동의 수혜를 받아 더 많은 주문을 받을 수 있을 것입니다.""",
    """AquaDew는 향후 2년 내에 일본, 중국, 동남아 시장 진출을 목표로 하고 있습니다. 이러한 글로벌 확장은 귀사와의 장기적인 협력 관계를 통해 이루어질 것이며,
    이는 귀사의 국제적 입지를 강화하는 데 기여할 것입니다. 우리의 글로벌 시장 진출은 귀사의 생산량 증가와 함께 안정적인 수익을 보장할 것입니다.""",
    """AquaDew는 오프라인 매장 확대를 위한 전략적 파트너십을 구축하고 있습니다. 이는 귀사와의 협력을 통해 오프라인 유통망을 강화하고, 
    더 많은 소비자에게 제품을 제공할 수 있는 기회를 창출할 것입니다. 
    오프라인 매장 확대는 귀사의 생산량 증가로 이어질 것이며, 이는 귀사의 수익성 향상에 기여할 것입니다.""",
    """AquaDew는 보습과 관련된 최신 연구 결과를 지속적으로 반영하고 있으며, 브랜드 신뢰도를 높이기 위해 전문 피부과와 협업도 계획 중입니다. 
    이러한 연구와 협업은 제품의 품질을 높이고, 
    소비자 신뢰를 강화하여 판매량 증가로 이어질 것입니다. 귀사는 이러한 품질 향상의 혜택을 받아 더 많은 주문을 받을 수 있을 것입니다.""",
    """AquaDew의 철학은 ‘수분을 지키는 것이 피부를 지키는 것이다’입니다. 이러한 철학은 우리의 모든 제품 개발에 반영되어 있으며, 
    이는 귀사와의 협력을 통해 더욱 강화될 것입니다. 
    우리의 철학은 제품의 차별성을 높이고, 소비자에게 더 큰 가치를 제공하여 판매량 증가로 이어질 것입니다.""",
    """AquaDew의 조민혁 대표는 화장품 업계에서 15년 이상의 경력을 쌓았으며, 그의 연구 논문은 국제 화장품 학회에서 발표되었습니다. 
    이러한 전문성은 브랜드의 신뢰성을 높이고, 귀사와의 협력을 통해 더욱 강화될 것입니다. 
    우리의 전문성은 제품의 품질을 높이고, 소비자 신뢰를 강화하여 판매량 증가로 이어질 것입니다.""",
]


class NegotiationBot:
    def __init__(self, min_price=2700, max_price=3000, beta=0.5, steps_for_brand=7):
        self.min_price = min_price
        self.max_price = max_price
        self.beta = beta
        self.N = steps_for_brand
        self.current_step = 1
        self.current_price = None
        self.negotiation_finished = False
        self.waiting_for_user_price = False
        self.waiting_for_final_price = False
        self.user_price = None
        self.final_user_price = None

    def propose_price(self):
        if self.current_step == 1:
            self.current_price = self.min_price - 100
            return f"""
            안녕하세요! 담당자님 AquaDew브랜드사의 Water 프로젝트를 담당하게 된 DealMakers AI 입니다.
            이번 협상을 통해 인사드리게 되어 영광이며, 성공적인 협상 과정을 통해 양사 모두가 좋은 결과를 가져갔으면 합니다.

            안내드린 PDF 파일 내용 내 컨셉의 제품을 MOQ 3,000개와 3개월 이내에 제품 출시를 목표하고 있습니다.

            이에 먼저 저희의 MOQ 및 3개월 이내에 맞춘 자사의 목표 단가는 2,600원 입니다. 
            
            {self.current_price}원에 맞춰주실 수 있을까요?"""

        elif self.current_step == 2:
            self.current_price = self.min_price
            return f"""
            {self.current_price}원에 맞춰주실 수 있을까요?"""

        else:
            if self.current_price is None:
                self.current_price = self.min_price
            info_idx = self.current_step - 3

            new_price = calculate_price(
                current_price=self.current_price,
                step_idx=self.current_step,
                base_min=self.min_price,
                base_max=self.max_price,
                beta=self.beta,
                N=self.N,
            )

            if self.user_price is not None and new_price >= self.user_price:
                self.negotiation_finished = True
                return f"""
    ✅ 협상 종료

    MOQ : 3000개 

    납품 기한 : 3개월 이내

    단가 : **{self.user_price}원**으로 협상을 마무리합니다.
    """
            else:
                self.current_price = new_price
                response = ""

                # 초기 3단계까지만 상위 % 표시
                if 3 <= self.current_step <= int(self.N / 2) + 2:
                    percentage = ((self.current_step - 2) * 100) / 9
                    response += f"📊 현재 제안 가격은 상위 **{percentage:.1f}%** 수준입니다.\n\n"

                if 0 <= info_idx < len(BRAND_INFO):
                    response += f"{BRAND_INFO[info_idx]}\n\n"

                response += f"**{self.current_price}**원에 맞춰주실 수 있을까요?"

                return response

    def accept(self):
        self.negotiation_finished = True
        return f"""
협상이 종료되었습니다.

✅ 최종 협상 금액: {self.current_price}원

✅ MOQ: 3,000개

✅ 납품 기한: 3개월 이내
"""

    def reject(self):
        if self.current_step == 1:
            self.current_step = 2
            return self.propose_price()
        elif self.current_step == 2:
            self.waiting_for_user_price = True
            return (
                "현재 저희 조건에서 조정할 수 있는 부분을 검토해보겠습니다. \n\n혹시 최종적으로 받아들이실 수 있는 가격대를 알려주실 수 있을까요?\n\n"
                "원하시는 단가를 입력해주세요."
            )
        elif 3 <= self.current_step < 9:
            self.current_step += 1
            return self.propose_price()
        else:
            self.waiting_for_final_price = True
            return (
                "다시 한 번 고려해주실 수 있나요?\n\n" "원하시는 단가를 입력해주세요:"
            )

    def process_user_price(self, val):
        self.user_price = val
        self.waiting_for_user_price = False
        self.current_step = 3
        self.current_price = None
        return f"사용자 희망가 {val}원 입력 받았습니다.\n\n" f"{self.propose_price()}"

    def process_final_price(self, val):
        self.final_user_price = val
        self.waiting_for_final_price = False
        self.negotiation_finished = True
        return f"""
다시 한 번 고려해주셔서 감사합니다.

협상 마무리하겠습니다.

✅ 최종 협상 금액: {self.final_user_price}원

✅ MOQ: 3,000개

✅ 납품 기한: 3개월 이내
"""


def main():
    st.title("DealMakers Nego Agent")

    if "bot" not in st.session_state:
        st.session_state.bot = NegotiationBot()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    bot = st.session_state.bot

    # 첫 제안은 한 번만 실행
    if "first_proposal_done" not in st.session_state:
        msg = bot.propose_price()
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.session_state.should_stream = True
        st.session_state.first_proposal_done = True

    # 모든 메시지 표시 (마지막 새 메시지만 스트리밍)
    for i, m in enumerate(st.session_state.messages):
        with st.chat_message(m["role"]):
            # 새로 추가된 마지막 메시지만 스트리밍
            if i == len(st.session_state.messages) - 1 and st.session_state.get(
                "should_stream", False
            ):
                stream_text(m["content"])
                if i == len(st.session_state.messages) - 1:
                    st.session_state.should_stream = False
            else:
                st.markdown(m["content"])

    if bot.negotiation_finished:
        with st.chat_message("assistant"):
            stream_text(
                f"이 조건으로 협상을 마무리하겠습니다. \n\n원활한 진행을 위해 이후 절차도 함께 협의해 나가길 기대합니다. \n\n감사합니다."
            )
        st.stop()

    if bot.waiting_for_final_price:
        with st.form(key="final_price_form"):
            val = st.number_input(
                "최종 희망가격 입력", min_value=1, max_value=999999, step=50
            )
            confirm = st.form_submit_button("입력하기")
            if confirm:
                user_msg = f"(최종 사용자 희망가격) {val}원"
                st.session_state.messages.append({"role": "user", "content": user_msg})
                resp = bot.process_final_price(val)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.session_state.should_stream = True
                st.rerun()
    elif bot.waiting_for_user_price:
        with st.form(key="user_price_form"):
            val = st.number_input(
                "희망가격 입력", min_value=1, max_value=999999, step=50
            )
            confirm = st.form_submit_button("입력하기")
            if confirm:
                user_msg = f"(사용자 희망가격) {val}원"
                st.session_state.messages.append({"role": "user", "content": user_msg})
                resp = bot.process_user_price(val)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.session_state.should_stream = True
                st.rerun()
    else:
        with st.form(key=f"step_form_{bot.current_step}"):
            decision = st.radio(
                f"{bot.current_step}단계 제안에 대한 결정:", ("YES", "NO"), index=1
            )
            if st.form_submit_button("Confirm"):
                st.session_state.messages.append({"role": "user", "content": decision})
                if decision == "YES":
                    resp = bot.accept()
                else:
                    resp = bot.reject()
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.session_state.should_stream = True
                st.rerun()


# 사이드바 : 주의사항 추가
with st.sidebar:
    st.title("⚠️주의사항")
    st.warning(
        "1. MOQ와 납품기한 등은 고정사항이므로,이 요건을 참조하여 단가 협상을 진행해주세요.\n\n"
        "2. 지시사항을 잘 보고 선택(입력)해주세요.\n\n"
        "3. 잘못입력하신 부분이 있다면 담당자에게 연락을 주세요.\n\n"
        "4. AI가 실시간으로 답변을 하므로 약간의 지체가 있을 수 있습니다."
    )
    with st.sidebar:
        show_contact = st.toggle("📞담당자 연락처 보기")

        # 토글 버튼의 상태에 따라 연락처 정보 표시
    if show_contact:
        st.sidebar.write("이름: 준성")
        st.sidebar.write("이메일: jun@dealmakers.co.kr")
        st.sidebar.write("전화번호: 010-1234-5678")


if __name__ == "__main__":
    main()
