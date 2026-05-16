"""Auth + landing. Calm healthcare aesthetic — soft palette, sticky nav,
hero with illustration, and the full set of guide-style sections."""

from datetime import datetime
import time

import streamlit as st

from core.session import clear_auth, remember_session
from core.styling import INK, SIGNAL, TINT_BLUE
from repositories.sessions import create_session
from repositories.users import add_user, verify_user
from ui.components import (
    article_card,
    doctor_card,
    guide_card,
    section_header_v2,
    testimonial_card,
)
from ui.illustrations import (
    BRAND_MARK_SVG,
    HERO_HEALTHCARE_SVG,
    category_glyph,
    FEATURE_ANALYTICS_SVG,
    FEATURE_CHAT_SVG,
    FEATURE_HOSPITAL_SVG,
)


def render_auth_gate() -> None:
    # Sticky-nav "Sign in" link sets ?auth=1; promote it to session state and
    # drop just that key (don't clobber a ?session= token that may also be present).
    if st.query_params.get("auth") == "1":
        st.session_state["show_auth"] = True
        st.query_params.pop("auth", None)
    if st.session_state.get("show_auth"):
        _render_auth_screen()
    else:
        _render_landing()


# ---------- shared chrome ----------

def _site_nav() -> None:
    st.markdown(
        f"<div class='site-nav' role='navigation'>"
        f"<div class='brand'>{BRAND_MARK_SVG}<span>MediGuide</span></div>"
        f"<div class='links'>"
        f"<a href='#guides'>Health guides</a>"
        f"<a href='#symptoms'>Symptoms</a>"
        f"<a href='#articles'>Articles</a>"
        f"<a href='#doctors'>Find a doctor</a>"
        f"<a href='#faq'>FAQ</a>"
        f"</div>"
        f"<a class='signin' href='?auth=1' target='_self'>Sign in</a>"
        f"</div>",
        unsafe_allow_html=True,
    )


def _brand_bar(meta: str = "v1.0 — healthcare guide") -> None:
    st.markdown(
        f"<div class='brand-bar'>"
        f"<div class='mark'>{BRAND_MARK_SVG}<span>MediGuide</span></div>"
        f"<div class='meta'>{meta}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def _footer() -> None:
    year = datetime.now().year
    st.markdown(
        "<div class='footer-grid'>"
        "  <div class='brand-col'>"
        f"   <div style='display:flex;align-items:center;gap:8px;font-weight:700;color:{INK};'>"
        f"     {BRAND_MARK_SVG}<span>MediGuide</span>"
        "   </div>"
        "   <p>Clear, trustworthy guidance on the cost and care of common medical procedures. "
        "Built with hospitals, clinicians, and patient educators.</p>"
        "  </div>"
        "  <div>"
        "    <h5>Product</h5>"
        "    <ul>"
        "      <li><a href='#'>Cost estimator</a></li>"
        "      <li><a href='#guides'>Medical guides</a></li>"
        "      <li><a href='#symptoms'>Symptom checker</a></li>"
        "      <li><a href='#doctors'>Doctor consultations</a></li>"
        "    </ul>"
        "  </div>"
        "  <div>"
        "    <h5>Resources</h5>"
        "    <ul>"
        "      <li><a href='#articles'>Health articles</a></li>"
        "      <li><a href='#faq'>FAQ</a></li>"
        "      <li><a href='#'>Patient stories</a></li>"
        "      <li><a href='#'>For clinicians</a></li>"
        "    </ul>"
        "  </div>"
        "  <div>"
        "    <h5>Contact</h5>"
        "    <ul>"
        "      <li>support@mediguide.health</li>"
        "      <li>+1 (415) 555-0142</li>"
        "      <li>Mon–Fri · 8am–8pm ET</li>"
        "    </ul>"
        "  </div>"
        "</div>"
        "<div class='footer-bottom'>"
        f"  <span>&copy; {year} MediGuide Inc. — Not a substitute for professional medical advice.</span>"
        "  <span class='legal'>"
        "    <a href='#'>Privacy</a>"
        "    <a href='#'>Terms</a>"
        "    <a href='#'>HIPAA</a>"
        "    <a href='#'>Accessibility</a>"
        "  </span>"
        "</div>",
        unsafe_allow_html=True,
    )


def _colophon() -> None:
    """Simple footer used on the auth screen."""
    year = datetime.now().year
    st.markdown(
        f"<div class='colophon'>"
        f"<span>&copy; {year} MediGuide Inc.</span>"
        f"<span class='colophon-links'>"
        f"<a href='#'>Privacy Policy</a>"
        f"<a href='#'>Terms of Service</a>"
        f"<a href='#'>HIPAA Compliance</a>"
        f"</span>"
        f"</div>",
        unsafe_allow_html=True,
    )


# ---------- landing ----------

def _render_landing() -> None:
    _site_nav()

    _hero()
    _trust_strip()
    _section_guides()
    _section_symptoms()
    _section_cost_transparency()
    _section_articles()
    _section_doctors()
    _section_testimonials()
    _section_faq()
    _footer()


def _hero() -> None:
    left, right = st.columns([6, 5], gap="large")
    with left:
        st.markdown(
            "<div style='padding: 28px 0 8px 0;'>"
            "<span class='hero-eyebrow'><span class='dot'></span>Trusted by 207 hospitals</span>"
            "<h1 class='hero-title'>Plan your care with clarity, before you walk in.</h1>"
            "<p class='hero-subtitle'>"
            "MediGuide brings together transparent cost estimates, plain-language medical guides, "
            "and verified specialists — so you can make care decisions with confidence."
            "</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        # Both CTAs are native anchors. "Check my estimate" uses ?auth=1 —
        # render_auth_gate promotes that to show_auth on the next pass. "Browse
        # health guides" is a hash link that smooth-scrolls to #guides. Plain
        # anchors avoid Streamlit's button mechanism (no rerun lag, no need
        # to thread session state through, real hover & focus behaviour).
        st.markdown(
            "<div class='hero-ctas'>"
            "<a class='cta primary' href='?auth=1' target='_self'>Check my estimate</a>"
            "<a class='cta secondary' href='#guides'>Browse health guides</a>"
            "</div>",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"<div class='hero-illus'>{HERO_HEALTHCARE_SVG}</div>",
            unsafe_allow_html=True,
        )


def _trust_strip() -> None:
    st.markdown(
        "<div class='trust-row'>"
        "<div class='trust-item'><span class='check'>✓</span> 207 partner hospitals</div>"
        "<div class='trust-item'><span class='check'>✓</span> 94% estimate accuracy</div>"
        "<div class='trust-item'><span class='check'>✓</span> HIPAA compliant</div>"
        "<div class='trust-item'><span class='check'>✓</span> Updated monthly</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def _section_guides() -> None:
    st.markdown(
        section_header_v2(
            "Medical guides",
            "Find clear answers, by specialty.",
            "Browse plain-language overviews of common procedures, conditions, and what to expect — "
            "written with clinicians, reviewed for accuracy.",
            anchor="guides",
        ),
        unsafe_allow_html=True,
    )

    # Each card opens an authoritative MedlinePlus topic page in a new tab —
    # real content, no maintenance, no signup required.
    categories = [
        ("Cardiology",   "Heart, vessels, and circulation. Includes bypass, stents, and ongoing cardiac care.", "blue", "https://medlineplus.gov/heartdiseases.html"),
        ("Orthopedics",  "Joints, bones, and recovery. Knee, hip, and shoulder procedures explained simply.",   "teal", "https://medlineplus.gov/boneinfectionsanddisorders.html"),
        ("Maternal Care","Prenatal through postpartum. What to plan for during pregnancy and delivery.",        "warm", "https://medlineplus.gov/pregnancy.html"),
        ("Pediatrics",   "From newborn checkups to teen wellness. Care guides written for parents.",            "blue", "https://medlineplus.gov/childrenshealth.html"),
        ("Mental Health","Therapy, medication options, and how to find the right kind of support.",             "teal", "https://medlineplus.gov/mentalhealth.html"),
        ("Oncology",     "Diagnosis, treatment paths, and second opinions for cancer-related care.",            "warm", "https://medlineplus.gov/cancers.html"),
    ]
    cards_html = "".join(
        guide_card(category_glyph(name), name, body, tone=tone, href=href)
        for name, body, tone, href in categories
    )
    st.markdown(f"<div class='guide-grid'>{cards_html}</div>", unsafe_allow_html=True)


def _section_symptoms() -> None:
    st.markdown(
        section_header_v2(
            "Symptoms checker",
            "Not sure what you're feeling? Start here.",
            "Answer a few short questions and we'll suggest what kind of care to consider, "
            "from self-care steps to when to see a specialist. This isn't a diagnosis — "
            "it's a starting point.",
            anchor="symptoms",
        ),
        unsafe_allow_html=True,
    )
    copy_col, card_col = st.columns([1, 1], gap="large")
    with copy_col:
        st.markdown(
            "<div class='symptom-copy'>"
            f"<h3 style='margin:0 0 10px 0; color: {INK};'>What we'll ask about</h3>"
            "<p style='color:#5B7185; font-size:14.5px; line-height:1.6; margin:0 0 4px 0;'>"
            "A short, structured intake — about three minutes.</p>"
            "<ul>"
            "  <li>How long the symptom has lasted, and how intense it feels</li>"
            "  <li>Any related conditions or recent procedures</li>"
            "  <li>Medications you take, and any allergies</li>"
            "  <li>Your age, sex, and relevant lifestyle context</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Try the assistant", key="symptoms_cta", use_container_width=False):
            st.session_state["show_auth"] = True
            st.rerun()
    with card_col:
        st.markdown(
            "<div class='symptom-card' aria-label='Sample symptom checklist'>"
            "  <div style='font-size:13px; color:#5B7185; font-weight:600; margin-bottom:8px;'>SAMPLE — chest discomfort</div>"
            "  <div class='row'><span class='chk on'>✓</span> Pain is sharp, lasting under 5 minutes</div>"
            "  <div class='row'><span class='chk on'>✓</span> No shortness of breath</div>"
            "  <div class='row'><span class='chk'></span> Pain radiates to the left arm</div>"
            "  <div class='row'><span class='chk'></span> Recent strenuous activity</div>"
            "  <div class='meta'>Next: we'll ask about prior cardiac history.</div>"
            "</div>",
            unsafe_allow_html=True,
        )


def _section_cost_transparency() -> None:
    st.markdown(
        section_header_v2(
            "Cost transparency",
            "Real prices, drawn from real invoices.",
            "We analyse anonymised closed-case invoices from our partner hospitals — "
            "so the estimate you see reflects what patients actually pay.",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='stats-grid'>"
        "<div class='stat-card'>"
        "<div class='stat-value'><span class='accent'>$24,310</span></div>"
        "<div class='stat-label'>Average surgical episode</div>"
        "</div>"
        "<div class='stat-card'>"
        "<div class='stat-value'>50,124</div>"
        "<div class='stat-label'>Estimates generated</div>"
        "</div>"
        "<div class='stat-card'>"
        "<div class='stat-value'>207</div>"
        "<div class='stat-label'>Partner hospitals</div>"
        "</div>"
        "<div class='stat-card'>"
        "<div class='stat-value'><span class='accent'>94.2%</span></div>"
        "<div class='stat-label'>Prediction accuracy</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def _section_articles() -> None:
    st.markdown(
        section_header_v2(
            "Health articles",
            "Reading worth your time.",
            "Short, practical articles from clinicians and patient educators — "
            "no jargon, no fluff.",
            anchor="articles",
        ),
        unsafe_allow_html=True,
    )
    articles = [
        (
            "Preparation",
            "What to bring to a pre-surgical consult",
            "A small amount of preparation saves hours of back-and-forth. Here's the short list "
            "your surgeon's office actually needs.",
            5,
            FEATURE_HOSPITAL_SVG,
            "https://medlineplus.gov/ency/patientinstructions/000459.htm",
        ),
        (
            "Insurance",
            "Reading your hospital invoice without panic",
            "Five line items that look scary but usually aren't, and three that genuinely deserve "
            "a phone call before you pay.",
            7,
            FEATURE_ANALYTICS_SVG,
            "https://www.cms.gov/medical-bill-rights",
        ),
        (
            "Recovery",
            "The week after a knee replacement",
            "What's typical, what's worth a call to your surgeon, and a realistic timeline for "
            "getting back to daily routines.",
            6,
            FEATURE_CHAT_SVG,
            "https://medlineplus.gov/ency/patientinstructions/000358.htm",
        ),
    ]
    cards_html = "".join(
        article_card(tag, title, excerpt, mins, thumb, href=href)
        for tag, title, excerpt, mins, thumb, href in articles
    )
    st.markdown(f"<div class='article-grid'>{cards_html}</div>", unsafe_allow_html=True)


def _section_doctors() -> None:
    st.markdown(
        section_header_v2(
            "Doctor consultations",
            "Talk to a specialist when you need one.",
            "Book a 20-minute video consultation with a verified specialist. "
            "Use it for a second opinion, a pre-procedure question, or to walk through your options.",
            anchor="doctors",
        ),
        unsafe_allow_html=True,
    )
    doctors = [
        ("AS", "Dr. Aditi Sharma, MD", "Cardiology · 14 yrs", True),
        ("MR", "Dr. Marcus Reeve, MD", "Orthopedic surgery · 18 yrs", True),
        ("JL", "Dr. Jamie Liu, MD", "Internal medicine · 9 yrs", False),
    ]
    cards_html = "".join(
        doctor_card(initials, name, spec, avail)
        for initials, name, spec, avail in doctors
    )
    st.markdown(f"<div class='doctor-grid'>{cards_html}</div>", unsafe_allow_html=True)
    a, _, _ = st.columns([1, 1, 1])
    with a:
        if st.button("Find a specialist", key="doctors_cta", use_container_width=True):
            st.session_state["show_auth"] = True
            st.rerun()


def _section_testimonials() -> None:
    st.markdown(
        section_header_v2(
            "What patients say",
            "Real stories from people who used MediGuide.",
        ),
        unsafe_allow_html=True,
    )
    quotes = [
        (
            "I had no idea you could see the actual price before showing up. The estimate "
            "for my husband's procedure came in within $400 of the final bill.",
            "Elena Rodriguez", "Houston, TX", "ER",
        ),
        (
            "The symptom checker pointed me to a cardiologist when I'd been writing it off "
            "as heartburn for weeks. Genuinely glad I tried it.",
            "David Park", "Seattle, WA", "DP",
        ),
        (
            "Used the cost comparison before my knee replacement. Saved nearly $6,000 by "
            "going with a different in-network hospital.",
            "Mary Thompson", "Atlanta, GA", "MT",
        ),
    ]
    cards_html = "".join(
        testimonial_card(q, name, role, initials)
        for q, name, role, initials in quotes
    )
    st.markdown(
        f"<div class='testimonial-wrap'><div class='testimonial-grid'>{cards_html}</div></div>",
        unsafe_allow_html=True,
    )


def _section_faq() -> None:
    st.markdown(
        section_header_v2(
            "Frequently asked",
            "Answers to what people ask us most.",
            anchor="faq",
        ),
        unsafe_allow_html=True,
    )
    faqs = [
        (
            "How accurate is the estimate, really?",
            "Based on a 12-month backtest against more than 5,000 closed invoices, our median "
            "absolute error is 6.1%. We show a confidence range alongside every estimate — "
            "especially for rarer procedures.",
        ),
        (
            "Where does the cost data come from?",
            "We partner with 200+ hospitals across 31 countries who share anonymised closed-case "
            "invoices each month, so estimates reflect what patients actually pay — not list prices.",
        ),
        (
            "Is my health data secure?",
            "Yes. We're fully HIPAA compliant. Uploads are processed in-session, never sold to "
            "third parties, and never used for advertising.",
        ),
        (
            "How do you make money?",
            "MediGuide is free for patients. We don't take referral fees from hospitals — our "
            "rankings are based purely on outcome quality and price fit.",
        ),
    ]
    faq_html = "".join(
        f"<div class='faq-item'>"
        f"<div class='faq-q'>{q}</div>"
        f"<div class='faq-a'>{a}</div>"
        f"</div>"
        for q, a in faqs
    )
    st.markdown(faq_html, unsafe_allow_html=True)


# ---------- auth screen ----------

def _render_auth_screen() -> None:
    _brand_bar()

    back_l, _ = st.columns([1.2, 6])
    with back_l:
        if st.button("← Back", key="auth_back"):
            st.session_state["show_auth"] = False
            st.rerun()

    # Center the auth form in a narrow column. Streamlit renders each call as
    # a sibling block, so a wrapping <div> in markdown doesn't actually contain
    # the inputs below it — st.columns is the only reliable centering primitive.
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(
            "<div class='cap sub' style='margin: 24px 0 6px 0;'>ACCESS</div>"
            "<h2 style='font-size:26px; margin:0 0 14px 0; letter-spacing:-0.015em;'>"
            "Welcome to MediGuide.</h2>"
            "<p style='color:#5B7185; font-size:15px; line-height:1.6; margin-bottom:18px;'>"
            "An account saves your estimates and uploaded reports between visits. "
            "You can also use the estimator without one — you just won't see history."
            "</p>",
            unsafe_allow_html=True,
        )
        auth_mode = st.radio(
            "Select Action",
            ["Sign in", "Create account"],
            horizontal=True,
            label_visibility="collapsed",
            key="auth_mode_radio",
        )
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        if auth_mode == "Sign in":
            _render_login()
        else:
            _render_signup()


def _render_login() -> None:
    user_input = st.text_input("Username", key="login_user", placeholder="your_username")
    pass_input = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
    if st.button("Sign in", key="login_btn"):
        with st.spinner("Checking..."):
            time.sleep(0.4)
            uid = verify_user(user_input, pass_input)
            if uid:
                st.session_state["user_id"] = uid
                st.session_state["username"] = user_input
                st.session_state["show_auth"] = False
                remember_session(create_session(uid))
                st.rerun()
            else:
                st.error("Wrong username or password.")


def _render_signup() -> None:
    new_user = st.text_input("Username", key="signup_user", placeholder="pick something")
    new_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
    new_pass = st.text_input("Password", type="password", key="signup_pass", placeholder="••••••••")
    if st.button("Create account", key="signup_btn"):
        if add_user(new_user, new_pass, new_email):
            st.success("Account created. Switch to Sign in to continue.")
        else:
            st.error("That username is taken or the inputs look off.")


# ---------- sidebar (post-login) ----------

def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:10px; margin:6px 0 24px 0;'>"
            f"  {BRAND_MARK_SVG}"
            f"  <span style='font-weight:700;letter-spacing:-0.01em;font-size:16px;color:{INK};'>"
            f"MediGuide</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='cap sub' style='margin-bottom:4px; font-size:11px;'>SIGNED IN AS</div>"
            f"<div style='font-weight:600; font-size:14px; color:{INK};'>"
            f"{st.session_state['username']}</div>"
            f"<div style='height:24px;'></div>",
            unsafe_allow_html=True,
        )


def render_logout() -> None:
    with st.sidebar:
        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
        if st.button("Log out", key="nav_logout"):
            clear_auth()
            st.rerun()
