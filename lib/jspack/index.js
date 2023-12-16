function sleep(delay, result) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(result)
    }, delay * 1000)
  })
}

export { sleep }