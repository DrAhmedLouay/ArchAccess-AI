# 🏛️ ArchAccess AI — Generative Architectural Universal Design & Bioclimatic Platform
### منصة الذكاء الاصطناعي التوليدي المعماري للتصميم الشامل والمحاكاة البيئية
**Developed and Designed by: Dr. Ahmed Louay**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ADA Standards 2010](https://img.shields.io/badge/ADA%20Compliance-100%25%20Gold-emerald.svg)](https://www.ada.gov/)

---

## 📌 نظرة عامة (Overview)
**ArchAccess AI** هي منصة رائدة قائمة على الذكاء الاصطناعي التوليدي المعماري والنمذجة الرياضية التوليدية، تهدف إلى **أتمتة إنتاج المساقط الأفقية السكنية التكيفية وفق معايير التصميم الشامل (Universal Design)** ومحددات الوصول لذوي الاحتياجات الخاصة ومستخدمي الكراسي المتحركة (**ADA Standards 2010**)، مع محاكاة دقيقة للمناخ العراقي والخصوصية الثقافية والاجتماعية.

---

## ✨ الخصائص والميزات الرئيسية (Key Capabilities)

1. **♿ الامتثال الحركي الصارم لكود الوصول الشامل (ADA Compliance & AGCR Metric):**
   - دوائر دوران حرة بقطر لا يقل عن **$\varnothing 1.50\text{ m}$ ($60"$)** في كافة الفضاءات.
   - ممر توزيع مركزي ومسار وصول رئيسي بعرض صافٍ لا يقل عن **$1.50\text{ m}$**.
   - جناح حمام مهيأ ($\ge 3.0\text{m} 	imes 3.0\text{m}$) مع حيز نقل جانبي ($1.50\text{m} 	imes 1.40\text{m}$)، شاور بدون عتبة (`Roll-in Shower`) مع مقعد قابل للطي وقضبان إمساك.
   - موقف سيارة مهيأ ($\ge 5.0\text{m} 	imes 2.0\text{m}$) مع حيز نزول سائق ذو إعاقة $1.80\text{m}$ وخلوص $30\text{cm}$.
   - منحدر صاعد مباشر إلى فضاء المعيشة بميل $1:12$ وعرض $\ge 1.20\text{m}$.

2. **☀️ المحاكاة المناخية التفاعلية للمحافظات العراقية (Iraq Bioclimatic GIS Simulation):**
   - محاكاة مسار الشمس الحقيقي لـ 18 محافظة عراقية (أوج الصيف $80.1^\circ$ وشمس الشتاء الدافئة $33.2^\circ$).
   - إسقاط الظلال المعمارية التفاعلية للكتل والجدران في الوقت الفعلي مع منزلق توقيت يومي ($06:00 - 18:00$).
   - مسارات الرياح السائدة الشمالية الغربية ($315^\circ\text{ NW}$) مع فناء داخلي ومنور تهوية طبيعية متصالبة.

3. **🧱 الضوابط البنائية والهندسية الموحدة (CAD-Grade Architectural Consistency):**
   - نسبة تغطية بنائية دقيقة ضمن النطاق المطلوب **$65\% \le \text{BCR} \le 75\%$**.
   - جدران مفردة موحدة بسماكة **$25\text{ cm}$** بدون تكرار.
   - فتحات أبواب صافية بعرض **$1.00\text{ m}$** مع كتف ارتداد ركني لا يزيد عن **$20\text{ cm}$**.
   - فضاء المعيشة وغرفة الضيوف بعرض صافٍ لا يقل عن **$4.00\text{ m}$**.
   - المطبخ وغرفة النوم بمساحات قياسية لا تقل عن **$3.0\text{m} \times 4.0\text{m}$**.

4. **🔄 حزمة التصدير والربط الهندسي (BIM, CAD, DXF, PDF):**
   - تصدير ملفات `DXF` ثنائية الأبعاد بطبقات معمارية قياسية.
   - تصدير بيانات نمذجة معلومات المباني `Revit BIM JSON`.
   - استخراج تقرير التدقيق المعماري الرسمي `ADA Audit Report` بصيغتي PDF و JSON.

---

## 🚀 النشر والتشغيل (Deployment & Quick Start)

### 1. التشغيل المحلي عبر Streamlit (Local Run)
```bash
# تثبيت المكتبات المطلوبة
pip install -r requirements.txt

# تشغيل التطبيق
streamlit run app.py
```

### 2. النشر على Streamlit Cloud
1. ارفع الكود إلى مستودع GitHub (`git push origin main`).
2. توجه إلى **[Streamlit Community Cloud](https://share.streamlit.io/)**.
3. اختر المستودع، وحدد الملف الرئيسي `app.py`.
4. اضغط **Deploy** ليصبح التطبيق متاحاً فوراً على الويب لجميع المستخدمين.

---

## 📊 مؤشرات البحث العلمي المحققة (Research Benchmarks)
* **مؤشر الامتثال الحركي (AGCR):** `100.0%` (الفئة الذهبية)
* **نسبة التغطية البنائية (BCR):** `69.8%` (ضمن نطاق 65% - 75%)
* **مؤشر التشابه الهيكلي (SSIM):** `0.7810`
* **متوسط الخطأ المطلق (MAE):** `0.0692`
* **زمن الاستدلال والتوليد:** `< 0.20 ثانية`

---

## 👨‍🏫 إعداد وتطوير (Author & Attribution)
**Developed and Designed by: Dr. Ahmed Louay**
*ArchAccess AI — Deep Generative Modeling for Architectural Accessibility & Universal Design.*
