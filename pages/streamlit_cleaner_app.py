import streamlit as st
import pandas as pd
import numpy as np
import io
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide", page_title="Red Bull Data Cleaner App")

st.title("🐂 Red Bull Data Cleaner App for Streamlit")
st.markdown("--- อัปโหลดไฟล์ CSV เพื่อทำความสะอาดข้อมูล Red Bull ---")
st.error("⚠️ แอปพลิเคชันนี้ออกแบบมาสำหรับไฟล์ CSV ที่มีโครงสร้างเหมือน redbull_workshop_dirty.csv เท่านั้น")

def clean_redbull_data(df_raw):
    """Performs all data cleaning steps on the Red Bull sales DataFrame."""

    df = df_raw.copy()

    st.subheader("✅ เริ่มต้นกระบวนการทำความสะอาดข้อมูล")
    st.info(f"ข้อมูลเริ่มต้น: {df.shape[0]:,} แถว, {df.shape[1]} คอลัมน์")

    # 1. Handle Duplicate Data
    initial_rows_dup = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_rows_dup:
        st.success(f"พบและลบข้อมูลซ้ำ: {initial_rows_dup - len(df):,} แถว. เหลือ {len(df):,} แถว")
    else:
        st.info("ไม่พบข้อมูลซ้ำ.")

    # 2. Handle Inconsistent Data
    st.subheader("🔄 2. การจัดการข้อมูลที่ไม่สอดคล้องกัน")

    # Standardize Region Column
    df['Region'] = df['Region'].str.strip().str.lower()
    region_mapping = {
        'th-central': 'TH-Central', 'th central': 'TH-Central',
        'thailand central': 'TH-Central', 'thailand-central': 'TH-Central',
        'thailand': 'TH-Central',
        'usa-east': 'USA-East', 'us east': 'USA-East',
        'united states east': 'USA-East', 'u.s.a.': 'USA-East',
        'europe-eu': 'Europe-EU', 'eu': 'Europe-EU',
        'europe': 'Europe-EU', 'european union': 'Europe-EU',
        'asia-pacific': 'Asia-Pacific', 'asia-pac': 'Asia-Pacific',
        'apac': 'Asia-Pacific', 'asia pacific': 'Asia-Pacific'
    }
    df['Region'] = df['Region'].replace(region_mapping)
    df['Region'] = df['Region'].str.upper()

    # Standardize Product_Variant Column
    df['Product_Variant'] = df['Product_Variant'].str.strip().str.lower()
    product_variant_mapping = {
        'original blue': 'Original Blue', 'original  blue': 'Original Blue',
        'krating daeng 250': 'Krating Daeng 250',
        'red edition': 'Red Edition',
        'sugarfree': 'Sugarfree', 'sugar free': 'Sugarfree',
        'sugarfree ': 'Sugarfree', 'sugar-free': 'Sugarfree',
        'tropical edition': 'Tropical Edition', 'tropical  edition': 'Tropical Edition',
        'tropical': 'Tropical Edition'
    }
    df['Product_Variant'] = df['Product_Variant'].replace(product_variant_mapping)

    # Standardize Channel Column
    df['Channel'] = df['Channel'].str.strip().str.lower()
    channel_mapping = {
        'social media': 'Social Media', 'social_media': 'Social Media',
        'tv ad': 'TV Ad', 'tv ads': 'TV Ad',
        'tv advertisement': 'TV Ad', 'television ad': 'TV Ad',
        'in-store promo': 'In-store Promo',
        'f1 sponsorship': 'F1 Sponsorship',
        'extreme sports': 'Extreme Sports'
    }
    df['Channel'] = df['Channel'].replace(channel_mapping)
    df['Channel'] = df['Channel'].apply(lambda x: x.title() if isinstance(x, str) else x)

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    st.success("แก้ไขข้อมูลที่ไม่สอดคล้องกันสำเร็จ.")

    # 3. Handle Missing Data
    st.subheader("📭 3. การจัดการข้อมูลที่หายไป")
    missing_before = df.isnull().sum().sum()
    if missing_before > 0:
        median_marketing = df['Marketing_Spend'].median()
        df['Marketing_Spend'] = df['Marketing_Spend'].fillna(median_marketing)
        median_score = df['Customer_Score'].median()
        df['Customer_Score'] = df['Customer_Score'].fillna(median_score)
        st.success(f"เติมเต็มค่าว่างจำนวน {missing_before:,} ค่า สำเร็จ.")
    else:
        st.info("ไม่พบข้อมูลที่หายไป.")

    # 4. Handle Noisy Data
    st.subheader("📢 4. การจัดการข้อมูลผิดพลาด (Noisy Data)")
    initial_rows_noisy = len(df)
    df = df[df['Unit_Price'] > 0]
    df = df[df['Units_Sold'] > 0]
    df = df[df['Marketing_Spend'] >= 0]
    df = df[(df['Customer_Score'] >= 1) & (df['Customer_Score'] <= 10)]
    if len(df) < initial_rows_noisy:
        st.success(f"ลบข้อมูลผิดพลาด (Noisy Data): ลบไป {initial_rows_noisy - len(df):,} แถว. เหลือ {len(df):,} แถว")
    else:
        st.info("ไม่พบข้อมูลผิดพลาด (Noisy Data) ที่ต้องลบ.")

    # 5. Outlier Detection (No treatment applied as per notebook decision)
    st.subheader("📐 5. การตรวจจับ Outlier (ไม่ปรับค่า)")
    st.info("ตามการวิเคราะห์ในโน้ตบุ๊ก จะไม่ทำการปรับ Outlier เพื่อรักษา Business Logic ของข้อมูล.")
    st.info(f"ข้อมูลหลังทำความสะอาด: {df.shape[0]:,} แถว, {df.shape[1]} คอลัมน์")

    return df

# --- File Uploader ---
uploaded_file = st.file_uploader("อัปโหลดไฟล์ CSV ของคุณที่นี่", type=["csv"])

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    st.write("### ข้อมูลดิบ (5 แถวแรก)")
    st.dataframe(df_raw.head())

    if st.button("เริ่มทำความสะอาดข้อมูล"): 
        with st.spinner('กำลังทำความสะอาดข้อมูล...'):
            df_cleaned = clean_redbull_data(df_raw)
            st.success("กระบวนการทำความสะอาดข้อมูลเสร็จสมบูรณ์!")

            st.write("### ข้อมูลที่ทำความสะอาดแล้ว (5 แถวแรก)")
            st.dataframe(df_cleaned.head())

            # Download Cleaned Data
            csv_buffer = df_cleaned.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="ดาวน์โหลดข้อมูลที่ทำความสะอาดแล้ว (CSV)",
                data=csv_buffer,
                file_name="redbull_clean.csv",
                mime="text/csv"
            )
else:
    st.info("กรุณาอัปโหลดไฟล์ CSV เพื่อเริ่มทำความสะอาดข้อมูล.")

if st.button("🏠 กลับหน้าหลัก"):
    st.switch_page("app.py")

