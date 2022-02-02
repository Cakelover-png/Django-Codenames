export function objToString(data) {
  let str = "";
  for (let [key, value] of Object.entries(data)) {
    str += `${key}=${value}&`;
  }
  console.log(str.substring(0, str.length - 1));
  return str.substring(0, str.length - 1);
}

export function setOrRemoveTokens(remove, access = null, refresh = null) {
  if (!remove) {
    if (!access) {
      localStorage.setItem("refresh", refresh);
    } else {
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
    }
  } else {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
  }
}

export function getXHR(url, headers) {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);

  for (const header of headers) {
    xhr.setRequestHeader(header[0], header[1]);
  }

  xhr.send(null);
  return xhr;
}

export function postXHR(url, headers, data) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);

  //Send the proper header information along with the request
  for (const header of headers) {
    xhr.setRequestHeader(header[0], header[1]);
  }

  xhr.send(objToString(data));
  return xhr;
}

export function postFormXHR(url, headers, data) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);

  //Send the proper header information along with the request
  for (const header of headers) {
    xhr.setRequestHeader(header[0], header[1]);
  }
}
