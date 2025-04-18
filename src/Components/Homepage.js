import React from "react";
import { Grid, Cell } from "react-mdl";

const Homepage = () => {
  return (
    <div style={{ width: "100%", margin: "auto" }}>
      <Grid className="homepage-grid">
        <Cell col={12}>
          <div className="profile-img-border">
            <img
              className="profile-img"
              src="images/DSC_5211-00.jpg"
              alt="Ismail"
            />
          </div>

          <div className="banner-text">
            <h1>Asp .Net Full Stack Developer</h1>
            <hr />
            <p>
              HTML | CSS | BOOTSTRAP | PHP | MYSQL | C# | ASP .NET CORE | SQL SERVER
            </p>

            <div className="social-links">
              {[
                {
                  href: "http://facebook.com/ismail96.12",
                  icon: "fa-facebook-official",
                },
                {
                  href: "https://twitter.com/ismail_miah_2",
                  icon: "fa-twitter-square",
                },
                {
                  href: "https://github.com/ismaelmiah",
                  icon: "fa-github-square",
                },
                {
                  href: "https://www.linkedin.com/in/ismaelmiah/",
                  icon: "fa-linkedin-square",
                },
              ].map(({ href, icon }) => (
                <a
                  key={icon}
                  href={href}
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  <i className={`fa ${icon}`} aria-hidden="true"></i>
                </a>
              ))}
            </div>
          </div>
        </Cell>
      </Grid>
    </div>
  );
};

export default Homepage;
