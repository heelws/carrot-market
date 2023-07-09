const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);
  //sha256 해시함수를 이용해서 프론트엔드에서 최소한의 암호화

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();

  //   if (res.status === 200) {
  //     alert("로그인 성공");
  //     window.location.pathname = "/";
  //   } else if (res.status === 401) {
  //     alert("id 혹은 password가 틀렸습니다");
  //   }
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인 성공");

  window.location.pathname = "/";

  //   const btn = document.createElement("button");
  //   btn.innerText = "상품 가져오기";

  //   btn.addEventListener("click", async () => {
  //     const res = await fetch("/items", {
  //       headers: {
  //         Authorization: `Bearer ${accessToken}`,
  //       },
  //     });
  //     const data = await res.json();
  //     console.log(data);
  //   });
  //   infoDiv.appendChild(btn);
};

form.addEventListener("submit", handleSubmit);
