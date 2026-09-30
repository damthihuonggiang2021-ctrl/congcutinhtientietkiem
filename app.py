import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# CSS GIAO DIỆN
# ==============================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #8B4513;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666666;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #FFF8F0;
        border: 1px solid #E6C9A8;
        margin-top: 15px;
    }

    .result-title {
        font-size: 18px;
        font-weight: bold;
        color: #8B4513;
    }

    .result-value {
        font-size: 25px;
        font-weight: bold;
        color: #A0522D;
    }
</style>
""", unsafe_allow_html=True)


# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ==============================
# TIÊU ĐỀ
# ==============================
st.markdown(
    '<div class="main-title">💰 TÍNH LÃI GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Tính toán tiền lãi theo phương pháp lãi đơn và lãi kép</div>',
    unsafe_allow_html=True
)


# ==============================
# NHẬP THÔNG TIN
# ==============================
st.header("📋 Thông tin khoản tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10000000.0,
    step=100000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

phuong_phap = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)


# ==============================
# NÚT TÍNH TOÁN
# ==============================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    # Kiểm tra dữ liệu
    if so_tien <= 0:
        st.error("❌ Số tiền gửi phải lớn hơn 0.")
        st.stop()

    if ky_han <= 0:
        st.error("❌ Kỳ hạn phải lớn hơn 0 tháng.")
        st.stop()

    if lai_suat < 0:
        st.error("❌ Lãi suất không được âm.")
        st.stop()

    # Chuyển lãi suất năm sang dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Thời gian tính theo năm
    thoi_gian_nam = ky_han / 12

    # ==========================================================
    # 1. LÃI ĐƠN
    # Công thức:
    # I = P × r × t
    # A = P + I
    # ==========================================================
    if phuong_phap == "Lãi đơn":

        tong_tien_lai = so_tien * lai_suat_nam * thoi_gian_nam
        tong_tien = so_tien + tong_tien_lai

        # --------------------------------------------
        # Lãi hàng tháng
        # --------------------------------------------
        if hinh_thuc == "Lãnh lãi hàng tháng":

            lai_dinh_ky = so_tien * lai_suat_nam / 12

            so_ky = ky_han

            ten_ky = "tháng"

        # --------------------------------------------
        # Lãi hàng quý
        # --------------------------------------------
        elif hinh_thuc == "Lãnh lãi hàng quý":

            lai_dinh_ky = so_tien * lai_suat_nam / 4

            so_ky = ky_han // 3

            ten_ky = "quý"

            # Nếu kỳ hạn không chia hết cho 3 tháng,
            # phần thời gian còn lại được tính riêng.
            thang_du = ky_han % 3

        # --------------------------------------------
        # Lãi cuối kỳ
        # --------------------------------------------
        else:

            lai_dinh_ky = tong_tien_lai

            so_ky = 1

            ten_ky = "kỳ"


    # ==========================================================
    # 2. LÃI KÉP
    # Tiền lãi được nhập vào gốc và tiếp tục sinh lãi.
    #
    # A = P × (1 + r/n)^(n×t)
    # ==========================================================
    else:

        # --------------------------------------------
        # Lãi kép hàng tháng
        # --------------------------------------------
        if hinh_thuc == "Lãnh lãi hàng tháng":

            so_ky = ky_han
            lai_suat_ky = lai_suat_nam / 12

            tong_tien = so_tien * (
                1 + lai_suat_ky
            ) ** so_ky

            tong_tien_lai = tong_tien - so_tien

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = so_tien * lai_suat_ky

            ten_ky = "tháng"

        # --------------------------------------------
        # Lãi kép hàng quý
        # --------------------------------------------
        elif hinh_thuc == "Lãnh lãi hàng quý":

            # Số quý đầy đủ
            so_quy = ky_han // 3

            # Số tháng còn dư
            thang_du = ky_han % 3

            lai_suat_quy = lai_suat_nam / 4

            # Tính sau các quý đầy đủ
            tong_tien = so_tien * (
                1 + lai_suat_quy
            ) ** so_quy

            # Tính phần tháng dư theo lãi suất tháng
            if thang_du > 0:
                lai_suat_thang = lai_suat_nam / 12

                tong_tien = tong_tien * (
                    1 + lai_suat_thang
                ) ** thang_du

            tong_tien_lai = tong_tien - so_tien

            # Lãi của quý đầu tiên
            lai_dinh_ky = so_tien * lai_suat_quy

            so_ky = so_quy

            ten_ky = "quý"

        # --------------------------------------------
        # Lãi kép cuối kỳ
        # --------------------------------------------
        else:

            # Tính theo số kỳ tháng để phù hợp kỳ hạn nhập
            lai_suat_thang = lai_suat_nam / 12

            tong_tien = so_tien * (
                1 + lai_suat_thang
            ) ** ky_han

            tong_tien_lai = tong_tien - so_tien

            lai_dinh_ky = tong_tien_lai

            so_ky = 1

            ten_ky = "kỳ"


    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.divider()

    st.header("📊 Kết quả tính toán")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền gốc",
            format_money(so_tien)
        )

    with col2:
        st.metric(
            "📈 Lãi suất",
            f"{lai_suat:.2f}%/năm"
        )

    # ------------------------------
    # Tiền lãi định kỳ
    # ------------------------------
    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-title">
                💸 Tiền lãi định kỳ
            </div>
            <div class="result-value">
                {format_money(lai_dinh_ky)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------
    # Tổng tiền lãi
    # ------------------------------
    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-title">
                📈 Tổng tiền lãi
            </div>
            <div class="result-value">
                {format_money(tong_tien_lai)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------
    # Tổng gốc + lãi
    # ------------------------------
    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-title">
                💰 Tổng số tiền gốc + lãi
            </div>
            <div class="result-value">
                {format_money(tong_tien)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==============================
    # THÔNG TIN CHI TIẾT
    # ==============================
    st.divider()

    st.subheader("📝 Thông tin khoản gửi")

    st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương pháp:** {phuong_phap}")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

    if hinh_thuc == "Lãnh lãi hàng tháng":
        st.info(
            f"Bạn nhận lãi theo chu kỳ **hàng tháng**. "
            f"Tiền lãi của kỳ đầu tiên là khoảng "
            f"**{format_money(lai_dinh_ky)}**."
        )

    elif hinh_thuc == "Lãnh lãi hàng quý":
        st.info(
            f"Bạn nhận lãi theo chu kỳ **hàng quý**. "
            f"Tiền lãi của một quý đầu tiên là khoảng "
            f"**{format_money(lai_dinh_ky)}**."
        )

    else:
        st.info(
            f"Bạn nhận toàn bộ tiền lãi khi **đáo hạn**. "
            f"Tổng tiền lãi nhận được là "
            f"**{format_money(tong_tien_lai)}**."
        )
