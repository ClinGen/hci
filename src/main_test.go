/*
Tests the code in the main module.
*/

package main

import (
	// Built-in libraries:
	"net/http"
	"net/http/httptest"
	"testing"

	// Third-party dependencies:
	"github.com/stretchr/testify/assert"
)

func TestIndexRoute(t *testing.T) {
	router := setupRouter()
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/", nil)
	router.ServeHTTP(w, req)
	assert.Equal(t, 200, w.Code)
	assert.Contains(t, w.Body.String(), "HCI")
}
