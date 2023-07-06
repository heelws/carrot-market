const form = document.getElementById("write-form");

const handlesubmitForm = async (event) => {
  event.preventDefault();
  const body = new FormData(form);
  //세계 시간 기준으로
  body.append("insertAt", new Date().getTime());

  try {
    const res = await fetch("/items", {
      method: "POST",
      body,
    });
    const data = await res.json();
    if (data === "200") window.location.pathname = "/";
  } catch (e) {
    console.error(e);
  }
  //try 안에서 로직 시도해보다가 error가 발생하면 catch 로직 실행
};

form.addEventListener("submit", handlesubmitForm);
