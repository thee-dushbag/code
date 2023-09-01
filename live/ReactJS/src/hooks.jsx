import { useState, useEffect } from "react";

export { useInput, useFetch, DataHook, useFetchJSON, useFetchBLOB };

function useInput(initialValue) {
  const [value, setValue] = useState(initialValue);
  return [
    { value, onChange: (e) => setValue(e.target.value) },
    () => setValue(initialValue),
  ];
}

function _baseUseFetch(url, fetcher = async (_) => _) {
  const [data, setData] = useState(undefined);
  const [error, setError] = useState(undefined);
  const [loading, setLoading] = useState(false);
  const _restoreDefaults = () => {
    setData(undefined);
    setError(undefined);
  };
  const fetchData = () => {
    if (!url) return;
    if (loading) return;
    _restoreDefaults();
    setLoading(true);
    fetcher(setData, setError).finally(() => setLoading(false));
  };
  useEffect(fetchData, [url]);
  return { data, error, loading, reload: fetchData };
}

function useFetchBLOB(url, init) {
  init = init || { method: "GET" };
  return _baseUseFetch(url, (onData, onError) =>
    fetch(url, init).then((resp) =>
      resp.ok ? resp.blob().then(onData) : resp.text().then(onError)
    )
  );
}

function useFetchJSON(url, init) {
  init = init || { method: "GET" };
  return _baseUseFetch(url, (onData, onError) =>
    fetch(url, init).then((resp) =>
      resp.ok ? resp.json().then(onData) : resp.text().then(onError)
    )
  );
}

function useFetch(url, init) {
  init = init || { method: "GET" };
  return _baseUseFetch(url, (onData, onError) =>
    fetch(url, init).then((resp) =>
      resp.ok ? resp.text().then(onData) : resp.text().then(onError)
    )
  );
}

function DataHook({
  onLoad = (_) => _,
  onData = (_) => _,
  onError = (_) => _,
  url,
  fetchInit,
  useFetchFunc = useFetchJSON,
}) {
  const { data, loading, error, reload } = useFetchFunc(url, fetchInit);
  if (loading) return onLoad();
  if (error) return onError(error, reload);
  return onData(data, reload);
}
