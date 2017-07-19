function parseErrorResponse(response) {
    const contentType = response.headers ?
          response.headers.map['Content-Type'] :
          []

    return contentType.includes('application/json') ?
        response.json() :
        Promise.resolve({'non_field_errors': ['Unknown error']})
}

function handleErrorResponse(component, errResponse) {
    console.log('handleErrorResponse')
    console.log(errResponse)
    return parseErrorResponse(errResponse)
        .then((errors) => {
            if (errors.detail) {
               errors['non_field_errors'] = errors.detail
            }
            component.$set(component.$data, 'errors', errors)
            console.log(errors)
        })
        .catch((err) => {
            console.error(err)
            component.$set(component.$data.errors, 'non_field_errors', ['Unknown error'])
        })
}

export {
    parseErrorResponse,
    handleErrorResponse
}
