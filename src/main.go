/*
The main module for the HCI. Defines routes. Drives the code.
*/

package main

import (
	// Built-in libraries:
	"fmt"
	"log"
	"net/http"
	"os"

	// Third-party dependencies:
	"github.com/gin-gonic/gin"
)

func setupRouter() *gin.Engine {
	router := gin.Default()

	// Get the absolute path to the HCI repo.
	hciRootDir, hciRootDirIsDefined := os.LookupEnv("HCI_ROOT_DIR")
	if !hciRootDirIsDefined {
		log.Fatal("HCI_ROOT_DIR is not defined; check your .env file")
	}

	// Load HTML templates.
	templatesDir := fmt.Sprintf("%s/src/templates/*", hciRootDir)
	router.LoadHTMLGlob(templatesDir)

	// Serve static files.
	staticDir := fmt.Sprintf("%s/src/static", hciRootDir)
	router.Static("/static", staticDir)

	// Define routes.
	router.GET("/", handleIndexGet)

	return router
}

func main() {
	router := setupRouter()
	err := router.Run(":8080")
	if err != nil {
		log.Print(err)
		log.Fatal("Unable to run the server; exiting")
	}
}

func handleIndexGet(c *gin.Context) {
	c.HTML(http.StatusOK, "base.html", gin.H{
		"Title":   "HCI",
		"Message": "Hello!",
	})
}
