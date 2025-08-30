import streamlit as st
from bs4 import BeautifulSoup

with open("candidates/odilbek_resume.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

name = soup.find("h1", class_="punjPpsdqoPsmHQibNXmdAxUKMhEDMdUIGvI inline t-24 v-align-middle break-words").text
summary = ""
experience = ""
education = ""
certification = ""

sections = soup.find_all("section", class_="artdeco-card pv-profile-card break-words mt2")

for section in sections:
    if section.find("div", id="about"):
        inner_div = section.find("div", class_="display-flex full-width")
        summary = inner_div.find("span", attrs={"aria-hidden": "true"}).text

    elif section.find("div", id="experience"):
        experiences = section.find_all("li", class_="artdeco-list__item lZKdEkCNDkuIWzkkoVlJKIpUQOwgnKJbmPmYMlExGQ fkQyJrHujYUIKEKjRRBeWPEGFVdNswiiuQ")
        for exp in experiences:
            job_title = exp.find("span", attrs={"aria-hidden": "true"}).text
            company = exp.find("span", class_="t-14 t-normal").span.text
            other_info = exp.find_all("span", class_="t-14 t-normal t-black--light")
            job_duration = other_info[0].span.text
            workplace = other_info[1].span.text
            experience = experience + job_title + "\n" + company + "\n" + job_duration + "\n" + workplace + "\n"

    elif section.find("div", id="education"):
        educations = section.find_all("li", class_="artdeco-list__item lZKdEkCNDkuIWzkkoVlJKIpUQOwgnKJbmPmYMlExGQ fkQyJrHujYUIKEKjRRBeWPEGFVdNswiiuQ")
        for edu in educations:
            institution = edu.find("div", class_="display-flex flex-wrap align-items-center full-height").find("span", attrs={"aria-hidden": "true"}).text
            description = edu.find("span", class_="t-14 t-normal").span.text
            education = education + institution + "\n" + description + "\n"

    elif section.find("div", id="licenses_and_certifications"):
        certifications = section.find_all("li", class_="artdeco-list__item lZKdEkCNDkuIWzkkoVlJKIpUQOwgnKJbmPmYMlExGQ fkQyJrHujYUIKEKjRRBeWPEGFVdNswiiuQ")
        for cert in certifications:
            cert_name = cert.find("div", class_="display-flex flex-wrap align-items-center full-height").find("span", attrs={"aria-hidden": "true"}).text
            cert_issuer = cert.find("span", class_="t-14 t-normal").span.text
            certification = certification + cert_name + "\n" + cert_issuer + "\n"


print(name)
print(summary)
print(experience)
print(education)
print(certification)
