function sleep(delay, result) {
  return Promise((resolve) => {
    setTimeout(() => {
      resolve(result)
    }, delay * 1000)
  })
}

export { sleep }